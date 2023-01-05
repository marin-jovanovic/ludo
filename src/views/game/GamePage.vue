<template>
  <!-- style="border-style: solid" -->

  <BaseUserTemplate>
    <TheMessages></TheMessages>
    <TheInfo ref="info"></TheInfo>

    <button @click="leaveGame">leave game</button>

    <div class="row">
      <div class="col">
        <TheGame></TheGame>
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
import { apiLevel } from "@/scripts/api/level";
import { acceptanceLogApi } from "@/scripts/api/acceptance_log";
import { wsListeners } from "@/scripts/ws_listener";
import { notification } from "@/scripts/notification";
import { setJoinIndex } from "@/scripts/set_playing_order";

/**
 * currentEntryIndex = 0
 *
 * try perform it, if can perfrom then advance to next index
 *
 */

export default {
  data() {
    return {
      username: "",
      gameId: "",
      log: undefined,

      // canRoll: false,
      // rollResult: -1,

      // instructionCurrentlyPerforming: -1,
      // lastInstructionPerformed: -1,

      // from playing order

      levelId: undefined,
      players: {},
      joinId: undefined,
      currentLogEntryIndex: undefined,
    };
  },
  async mounted() {
    this.levelId = this.$route.params.id;
    this.username = userMetaSS.getCredentials()["username"];

    await setJoinIndex(this.username, this.levelId);

    this.joinId = levelSessionStorage.getLevelMeta()["levelJoinIndex"];

    let capacity = levelSessionStorage.getLevelMeta()["capacity"];
    this.currentLogEntryIndex = await this.bypassGoes(this.levelId, capacity);

    // this is from playing order part

    let url = "ws://127.0.0.1:8000/acceptanceLogEntryCreated/";
    new wsListeners.WebSocketListener(url, this.wsReceive);

    // run condition, what if get then ws vs ws then get

    await this.loadPlayers();
    await this.loadLog();

    await this.loadConfirmationLog();

    await this.tryNextInstruction();

    // this.currentLogEntryIndex = 0;
    // let logEntry = this.log[this.currentLogEntryIndex];
    // this.players[logEntry.player].isTurn = true;
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

      // total count of people

      // res = await apiLevel.getSpecificLevel({
      //   levelId: levelId,
      // });

      // if (!(res["auth"]["status"] && res["payload"]["status"])) {
      //   console.log("err");
      //   return;
      // }

      // let joinToUsername = {};

      // for (const value of Object.values(res["payload"]["users"])) {
      //   joinToUsername[value.joinId] = {
      //     username: value.username,
      //   };
      // }

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

    async tryNextInstruction() {
      // setup
      let entryLogIndex = this.currentLogEntryIndex + 1;
      console.log("try", entryLogIndex);

      if (!(entryLogIndex in this.log)) {
        console.log("err? not in this.log");
        //         console.log("not in log, need to create new entries in be");
        // i assume that player needs to make a move
      }

      // main

      let logEntry = this.log[entryLogIndex];

      if (logEntry.action === "goes") {
        console.log("err goes");
      } else {
        console.log("can not perform on my own");
        console.log(logEntry);
        return;
      }

      // cleanup

      let isLogged = await this.sendConfirmation(this.log[entryLogIndex]);

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

      // await this.tryNextInstruction();
    },

    // passive actions
    async wsReceive(message) {
      console.log("received update", message);

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

      return res["payload"]["performedEntries"];
    },

    // if page refreshed
    async loadConfirmationLog() {
      let performedLogEntryIndexToId =
        await this.fetchPerformedLogEntryIndexToId();

      console.log(performedLogEntryIndexToId);

      console.log("starting confirmation log with", this.currentLogEntryIndex);

      // confirm everything before this
      for (let i = 0; i < this.currentLogEntryIndex + 1; i++) {
        console.log("auto confirm this", i, this.log[i].id);

        let isLogged = await this.sendConfirmation(this.log[i].id);

        if (!isLogged) {
          console.log("err sending confirmation");
        }
      }

      // add those instructions to performed entries
      // this is executed instead of calling again fetchPerformedLogEntryIndexToId
      for (let i = 0; i < this.currentLogEntryIndex + 1; i++) {
        console.log("auto add this", i, this.log[i].id);

        // todo check if something diff is here then this is not correctly implemented (possible error while sorting?)
        performedLogEntryIndexToId[i] = this.log[i].id;
      }

      // fast loading (updating board)
      for (const [i, entry] of Object.entries(this.log)) {
        if (Number(i) !== entry.instruction_id) {
          console.log("sorting error", Number(i), entry.instruction_id);
        }

        if (this.currentLogEntryIndex >= i) {
          console.log(
            "skip (pre goes instruction)",
            this.currentLogEntryIndex,
            i
          );
          continue;
        }

        if (!(i in performedLogEntryIndexToId)) {
          console.log("entry not yet performed", i, entry);
          break;
        }

        console.log(i, entry);

        // console.log("perform", entry.id);

        // switch (entry.action) {
        //   case "roll":
        //     break;
        //   case "goes":
        //     console.log("err goes");
        //     break;
        //   default:
        //     console.log("err unknown");
        //     break;
        // }

        // this.currentLogEntryIndex++;
      }

      console.log("currentLogEntryIndex", this.currentLogEntryIndex);

      // // set turn
      // let logEntry = this.log[this.currentLogEntryIndex];
      // this.players[logEntry.player].isTurn = true;
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
        console.log("err");
      }

      return flag;
    },

    async rollDice() {
      // setup
      let entryLogIndex = this.currentLogEntryIndex + 1;
      let logEntry = this.log[entryLogIndex];

      if (!(this.joinId === logEntry.player)) {
        console.log("not your turn");
        return;
      }

      if (logEntry.action !== "roll") {
        console.log("not roll action");
        return;
      }

      this.$refs.dice.rollDice(logEntry.diceResult);

      let isLogged = await this.sendConfirmation(this.log[entryLogIndex]);

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

      // backend needs to send to others this info
      // backend waits for all others to confirm (timeout)
    },

    async loadPlayers() {
      let res = await apiLevel.getSpecificLevel({ levelId: this.levelId });

      if (!(res["auth"]["status"] && res["payload"]["status"])) {
        console.log("err");
        return;
      }

      for (const [key, value] of Object.entries(res["payload"]["users"])) {
        // no need for isTurn -> todo remove
        this.players[value.joinId] = {
          username: value.username,
          isTurn: false,
          id: key,
        };
      }
    },

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
