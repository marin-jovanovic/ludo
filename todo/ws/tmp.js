<template>
  <!-- style="border-style: solid" -->

  <BaseUserTemplate>
    <TheMessages></TheMessages>
    <TheInfo ref="info"></TheInfo>

    <button @click="leaveGame">leave game</button>

    <div class="row">
      <div class="col">
        <TheGame @tokenSelected="userClickedOnToken" ref="level"></TheGame>
      </div>

      <div class="col">
        <div class="row">
          <div class="col">
            <TheDice ref="dice"></TheDice>
          </div>
          <div class="col">
            <button @click="rollDice">roll dice</button>
          </div>
        </div>
      </div>

      <div class="col">
        <h5>performed log:</h5>
      </div>
    </div>
  </BaseUserTemplate>
</template>


<script>
import TheInfo from "./TheInfo.vue";
import TheGame from "./TheGame.vue";
import TheDice from "@/components/TheDice.vue";

import BaseUserTemplate from "@/components/BaseUserTemplate.vue";
import TheMessages from "./TheMessages.vue";
import { apiLevelLog } from "@/scripts/api/level_log";

import { levelSessionStorage, userMetaSS } from "@/scripts/session_storage";
// import { apiLevel } from "@/scripts/api/level";
import { acceptanceLogApi } from "@/scripts/api/acceptance_log";
import { wsListeners } from "@/scripts/ws_listener";
import { notification } from "@/scripts/notification";
import { setJoinIndex } from "@/scripts/set_playing_order";

/**
 * currentEntryIndex = 0
 *
 * try perform it, if can perfrom then advance to next index
 *
 * this is different from dice order part
 *
 */

export default {
  data() {
    return {
      username: "",
      gameId: "",
      log: undefined,

      levelId: undefined,
      players: {},
      joinId: undefined,
      currentLogEntryIndex: undefined,
      globalPerformedLogEntryIndexToId: undefined,
      privatePerformedLogEntryIndexToId: undefined,
      isWaitingForUserToChooseToken: false,
    };
  },
  async mounted() {
    this.levelId = this.$route.params.id;
    this.username = userMetaSS.getCredentials()["username"];

    await setJoinIndex(this.username, this.levelId);

    this.joinId = levelSessionStorage.getLevelMeta()["levelJoinIndex"];

    let capacity = levelSessionStorage.getLevelMeta()["capacity"];
    this.currentLogEntryIndex = await this.bypassGoes(this.levelId, capacity);

    let url = "ws://127.0.0.1:8000/acceptanceLogEntryCreated/";
    new wsListeners.WebSocketListener(url, this.wsReceive);

    // run condition, what if get then ws vs ws then get

    // await this.loadPlayers();
    await this.loadLog();

    await this.loadConfirmationLog();

    await this.tryNextInstruction();
  },
  methods: {
    async bypassGoes(levelId, capacity) {
      // skip first part of the log where order is determined
      let res = await apiLevelLog.getLevelLog(levelId);

      if (!(res["auth"]["status"] && res["payload"]["status"])) {
        console.log("err");
        return;
      }

      let log = res["payload"]["log"];

      let c = 0;
      let logIndex = 0;
      for (const value of Object.values(log)) {
        if (value.action === "goes") {
          c++;
        }

        if (capacity === c) {
          break;
        }
        logIndex++;
      }

      if (capacity !== c) {
        console.log("err capacity !== c", capacity, c);
      }

      return logIndex;
    },

    // this is from playing order

    entrySetup() {
      let entryLogIndex = this.currentLogEntryIndex + 1;
      console.log(entryLogIndex);

      if (!(entryLogIndex in this.log)) {
        console.log("err? not in this.log");
        // i assume that player needs to make a move
      }

      let logEntry = this.log[entryLogIndex];
      return logEntry;
    },

    async entryCleanup(logEntry, payload = undefined) {
      console.log("entryCleanup");

      let isLogged = await this.sendConfirmation(logEntry.id, payload);

      notification.showMessage(
        isLogged,
        "move logged",
        "error logging to server"
      );

      if (isLogged) {
        // or this.currentLogEntryIndex = entryLogIndex
        this.currentLogEntryIndex++;
      } else {
        console.log("err");
      }
    },

    async tryNextInstruction() {
      console.log("try next instruction");
      let logEntry = this.entrySetup();

      if (logEntry.player !== this.joinId) {
        if (logEntry.instruction_id in this.globalPerformedLogEntryIndexToId) {
          console.log("master made this instruction");
        } else {
          console.log("need to wait for master player to log this move");
          return;
        }
      }

      // main

      if (logEntry.action === "goes") {
        console.log("err tryNextInstruction goes");
      } else if (logEntry.action === "move") {
        console.log("move", logEntry);

        if (this.joinId !== logEntry.player) {
          console.log("err not same", this.joinId, logEntry.player);
        }

        this.$refs.level.movePosition({
          player: logEntry.player,
          token: logEntry.token,
          jumpCount: logEntry.diceResult,
        });
      } else if (
        logEntry.player !== this.joinId &&
        logEntry.action === "roll"
      ) {
        console.log("roll");
        this.$refs.dice.rollDice(logEntry.diceResult);
      } else {
        console.log("tryNextInstruction can not perform on my own", logEntry);
        return;
      }

      this.entryCleanup(logEntry);
    },

    // passive actions
    async wsReceive(message) {
      console.log("received update", message);

      // todo check if this key exists then sorting problem (? assumption that this is cause)

      // todo this is not nice naming, change this to reflect it better
      this.globalPerformedLogEntryIndexToId[message.id] = message.entryId;

      await this.tryNextInstruction();

      // how does it know that it can contine?

      // let toAcceptIndex = message.entryId;

      // if (this.currentLogEntryIndex > Number(toAcceptIndex)) {
      //   console.log(this.currentLogEntryIndex, toAcceptIndex);
      //   console.log("mismatch, skip");
      //   await this.tryNextInstruction();
      //   return;
      // }

      // let logEntry = this.log[this.currentLogEntryIndex];
      // this.players[logEntry.player].isTurn = true;

      // if (logEntry.action === "roll") {
      //   // someone else performed this
      //   this.$refs.dice.rollDice(logEntry.diceResult);
      // }

      // this.currentLogEntryIndex++;
      // this.players[logEntry.player].isTurn = false;

      // // send to backend that it is performed
      // await this.sendConfirmation(this.currentLogEntryIndex - 1);

      // logEntry = this.log[this.currentLogEntryIndex];
      // this.players[logEntry.player].isTurn = true;

      // await this.tryNextInstruction();
    },

    async fetchPerformedLogEntryIndexToId() {
      let res = await acceptanceLogApi.getAcceptanceLogForLevel({
        levelId: this.levelId,
      });

      let flag = res["auth"]["status"] && res["payload"]["status"];

      if (!flag) {
        console.log("err");
      }

      console.log(res["payload"]);

      this.globalPerformedLogEntryIndexToId =
        res["payload"]["globalPerformedEntries"];
      this.privatePerformedLogEntryIndexToId =
        res["payload"]["performedEntries"];

      // console.log(Object.keys(res["payload"]["globalPerformedEntries"]).length);

      // console.log(Object.keys(res["payload"]["performedEntries"]).length);

      return res["payload"]["performedEntries"];
    },

    // if page refreshed
    async loadConfirmationLog() {
      let performedLogEntryIndexToId =
        await this.fetchPerformedLogEntryIndexToId();

      console.log("ui updated", Object.keys(performedLogEntryIndexToId));

      console.log("starting confirmation log with", this.currentLogEntryIndex);

      // confirm everything before this
      for (let i = 0; i < this.currentLogEntryIndex + 1; i++) {
        // console.log("auto confirm this", i, this.log[i].id);

        let isLogged = await this.sendConfirmation(this.log[i].id);

        if (!isLogged) {
          console.log("err sending confirmation");
        }
      }

      // add those instructions to performed entries
      // this is executed instead of calling again fetchPerformedLogEntryIndexToId
      for (let i = 0; i < this.currentLogEntryIndex + 1; i++) {
        // console.log("auto add this", i, this.log[i].id);

        // todo check if something diff is here then this is not correctly implemented (possible error while sorting?)
        performedLogEntryIndexToId[i] = this.log[i].id;
      }

      // fast loading (updating board)
      for (const [i, logEntry] of Object.entries(this.log)) {
        if (Number(i) !== logEntry.instruction_id) {
          console.log("sorting error", Number(i), logEntry.instruction_id);
        }

        if (this.currentLogEntryIndex >= i) {
          // console.log(
          //   "skip (pre goes instruction)",
          //   this.currentLogEntryIndex,
          //   i
          // );
          continue;
        }

        if (!(i in performedLogEntryIndexToId)) {
          // console.log("logEntry not yet performed", i, logEntry);
          break;
        }

        console.log("fast perform", i, logEntry);

        switch (logEntry.action) {
          case "roll":
            this.$refs.dice.rollDice(logEntry.diceResult);

            break;
          case "goes":
            console.log("err goes");
            break;

          case "move":
            if (this.joinId !== logEntry.player) {
              console.log("err not same", this.joinId, logEntry.player);
            }

            this.$refs.level.movePosition({
              player: logEntry.player,
              token: logEntry.token,
              jumpCount: logEntry.diceResult,
            });

            break;

          default:
            console.log("err unknown");
            break;
        }

        // this.currentLogEntryIndex++;
      }

      this.currentLogEntryIndex =
        Object.keys(performedLogEntryIndexToId).length - 1;

      console.log(
        "after fast reloading, last executed is",
        this.currentLogEntryIndex
      );

      // console.log(
      //   "after realoding, we can be sure this is performed:",
      //   Object.keys(this.privatePerformedLogEntryIndexToId),
      // );
    },

    async sendConfirmation(entryIndex, payload = undefined) {
      console.log("confirmation for", entryIndex, "todo", payload);

      let res = await acceptanceLogApi.addEntryToAcceptanceLog({
        levelId: this.levelId,
        entryId: entryIndex,
        payload: payload,
      });

      let flag = res["auth"]["status"] && res["payload"]["status"];

      if (!flag) {
        console.log("err", res);
      }

      return flag;
    },

    async rollDice() {
      // console.log(this.log);

      // console.log(this.currentLogEntryIndex);

      let logEntry = this.entrySetup();

      if (!(this.joinId === logEntry.player)) {
        console.log("not your turn");
        notification.showMessage(false, "", "not your turn");
        return;
      }

      if (logEntry.action !== "roll") {
        console.log("err not roll action", logEntry.action);
        return;
      }

      this.$refs.dice.rollDice(logEntry.diceResult);

      console.log(
        this.currentLogEntryIndex + 1,
        this.log,
        this.currentLogEntryIndex + 1 in this.log
      );

      if (
        !(this.currentLogEntryIndex + 1 + 1 in this.log) ||
        !(
          this.currentLogEntryIndex + 1 in
          this.privatePerformedLogEntryIndexToId
        )
      ) {
        console.log("assumption: user needs to decide");

        this.isWaitingForUserToChooseToken = true;
      } else {
        console.log("assumption: not used");

        this.entryCleanup(logEntry);
      }

      // todo what if user reloads page now?

      // no cleanup

      // backend needs to send to others this info
      // backend waits for all others to confirm (timeout)
    },

    async userClickedOnToken(username, tokenId) {
      // no need for additional checks, assumption is that they are run in previous function

      console.log("user clicked on token", username, tokenId);

      if (
        !(this.currentLogEntryIndex + 1 + 1 in this.log) ||
        !(
          this.currentLogEntryIndex + 1 in
          this.privatePerformedLogEntryIndexToId
        )
      ) {
        console.log("test: user needs to decide");

        this.isWaitingForUserToChooseToken = true;
      } else {
        console.log("test: not used");
      }

      // if (!this.isWaitingForUserToChooseToken) {
      //   console.log("not waiting for this");
      //   return;
      // }

      if (this.username !== username) {
        console.log(
          "not same usernmae, choose your tokens",
          this.username,
          username
        );
        return;
      }

      this.isWaitingForUserToChooseToken = false;

      // do this step again
      let logEntry = this.entrySetup();

      let t = await apiLevelLog.addToLog(this.levelId, tokenId);
      console.log(t);

      this.entryCleanup(logEntry, {
        instruction: "moveToken",
        username: username,
        tokenId: tokenId,
      });
    },

    // async loadPlayers() {
    //   let res = await apiLevel.getSpecificLevel({ levelId: this.levelId });

    //   if (!(res["auth"]["status"] && res["payload"]["status"])) {
    //     console.log("err", res);
    //     return;
    //   }

    //   for (const [key, value] of Object.entries(res["payload"]["users"])) {
    //     // no need for isTurn -> todo remove
    //     this.players[value.joinId] = {
    //       username: value.username,
    //       isTurn: false,
    //       id: key,
    //     };
    //   }
    // },

    async loadLog() {
      let res = await apiLevelLog.getLevelLog(this.levelId);

      if (!(res["auth"]["status"] && res["payload"]["status"])) {
        console.log("err");
        return;
      }

      console.log("log", res["payload"]["log"]);

      this.log = res["payload"]["log"];
    },
  },
  components: {
    TheInfo,
    TheDice,
    BaseUserTemplate,
    TheMessages,
    TheGame,
  },
};
</script> 
