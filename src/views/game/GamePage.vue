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
    </div>
  </BaseUserTemplate>
</template>


<script>
import TheInfo from "./TheInfo.vue";
import TheGame from "./TheGame.vue";
import TheDice from "@/components/TheDice.vue";

import BaseUserTemplate from "@/components/BaseUserTemplate.vue";
import { router } from "@/router/router";
import TheMessages from "./TheMessages.vue";
import { apiLevelLog } from "@/scripts/api/level_log";

import { levelSessionStorage, userMetaSS } from "@/scripts/session_storage";
import { apiLevel } from "@/scripts/api/level";
import { acceptanceLogApi } from "@/scripts/api/acceptance_log";
import { wsListeners } from "@/scripts/ws_listener";
import { notification } from "@/scripts/notification";
import { setJoinIndex } from "@/scripts/set_playing_order";

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
      order: [],
      capacity: undefined,
    };
  },
  async mounted() {
    this.levelId = this.$route.params.id;
    this.capacity = levelSessionStorage.getLevelMeta()["capacity"];
    this.username = userMetaSS.getCredentials()["username"];

    await setJoinIndex(this.username, this.levelId);

    this.joinId = levelSessionStorage.getLevelMeta()["levelJoinIndex"];

    await this.bypassGoes();

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
    async bypassGoes() {
      // skip first part of the log where order is determined
      let res = await apiLevelLog.getLevelLog(this.levelId);

      if (!(res["auth"]["status"] && res["payload"]["status"])) {
        console.log("err");
        return;
      }

      let log = res["payload"]["log"];

      // total count of people

      res = await apiLevel.getSpecificLevel({
        levelId: this.levelId,
      });

      if (!(res["auth"]["status"] && res["payload"]["status"])) {
        console.log("err");
        return;
      }

      let joinToUsername = {};

      for (const value of Object.values(res["payload"]["users"])) {
        joinToUsername[value.joinId] = {
          username: value.username,
        };
      }

      let c = 0;
      let logIndex = 0;
      for (const value of Object.values(log)) {
        if (value.action === "goes") {
          c++;
        }

        if (this.capacity === c) {
          break;
        }

        logIndex++;
      }

      if (this.capacity !== c) {
        console.log("err this.capacity !== c", this.capacity, c);
        console.log(typeof this.capacity, c);
      }

      this.currentLogEntryIndex = logIndex + 1;
      console.log("current", this.currentLogEntryIndex);
    },

    // this is from playing order

    goToLevel() {
      console.log("to game");

      router.replace(`/game/${this.levelId}`);
    },
    isOrderDetermined() {
      console.log("rec");
      return this.capacity === this.order.length;
    },

    async tryNextInstruction() {
      console.log("try");
      console.log(this.currentLogEntryIndex);

      let logEntry = this.log[this.currentLogEntryIndex];

      if (logEntry.action === "goes") {
        console.log("goes");
        console.log("err");
        this.order.push(this.players[logEntry.player].username);

        console.log("oder", this.isOrderDetermined());
      } else {
        console.log("can not perform on my own");
        console.log(logEntry);
        return;
      }

      this.currentLogEntryIndex++;

      await this.sendConfirmation(this.currentLogEntryIndex - 1);

      await this.tryNextInstruction();
    },

    // passive actions
    async wsReceive(message) {
      console.log("received update", message);

      let toAcceptIndex = message.entryId;

      if (this.currentLogEntryIndex > Number(toAcceptIndex)) {
        console.log(this.currentLogEntryIndex, toAcceptIndex);
        console.log("mismatch, skip");
        await this.tryNextInstruction();
        return;
      }

      let logEntry = this.log[this.currentLogEntryIndex];
      this.players[logEntry.player].isTurn = true;

      if (logEntry.action === "roll") {
        // someone else performed this
        this.$refs.dice.rollDice(logEntry.diceResult);
      }

      this.currentLogEntryIndex++;
      this.players[logEntry.player].isTurn = false;

      // send to backend that it is performed
      await this.sendConfirmation(this.currentLogEntryIndex - 1);

      logEntry = this.log[this.currentLogEntryIndex];
      this.players[logEntry.player].isTurn = true;

      await this.tryNextInstruction();
    },

    // if page refreshed
    async loadConfirmationLog() {
      let res = await acceptanceLogApi.getAcceptanceLogForLevel({
        levelId: this.levelId,
      });

      let flag = res["auth"]["status"] && res["payload"]["status"];

      if (!flag) {
        console.log("err");
      }

      let performedEntries = new Set();

      for (const entryIndex of Object.values(
        res["payload"]["performedEntries"]
      )) {
        performedEntries.add(entryIndex);
      }

      // load everything before goes

      let c = 0;
      for (const value of Object.values(this.log)) {
        console.log("execute entry", value);

        if (value.action === "goes") {
          c++;
        }

        if (this.capacity === c) {
          break;
        }
      }

      if (this.capacity !== c) {
        console.log("err this.capacity !== c", this.capacity, c);
        console.log(typeof this.capacity, c);
      }

      // fast loading

      for (const entry of Object.values(this.log)) {
        if (performedEntries.has(entry.id)) {
          console.log("perform", entry.id);

          switch (entry.action) {
            case "roll":
              console.log("roll");
              break;
            case "goes":
              console.log("err");
              console.log("goes");
              console.log(this.order);
              this.order.push(this.players[entry.player].username);
              console.log("order", this.isOrderDetermined());
              break;
            default:
              console.log("unknown");
              break;
          }

          this.currentLogEntryIndex++;
        } else {
          break;
        }
      }

      // set turn
      let logEntry = this.log[this.currentLogEntryIndex];
      this.players[logEntry.player].isTurn = true;
    },

    async sendConfirmation(entryIndex, payload = undefined) {
      console.log(payload);

      let res = await acceptanceLogApi.addEntryToAcceptanceLog({
        levelId: this.levelId,
        entryId: entryIndex,
      });

      let flag = res["auth"]["status"] && res["payload"]["status"];

      if (!flag) {
        console.log("err");
      }

      return flag;
    },

    async rollDice() {
      let logEntry = this.log[this.currentLogEntryIndex];

      if (!this.players[this.joinId].isTurn) {
        console.log("not your turn");
        return;
      }

      //   cleanup
      this.players[this.joinId].isTurn = false;

      if (logEntry.player !== this.joinId) {
        console.log("err: internal, not your turn");
        return;
      }

      if (logEntry.action !== "roll") {
        console.log("not roll action");
        return;
      }

      this.$refs.dice.rollDice(logEntry.diceResult);

      this.currentLogEntryIndex++;

      let isLogged = await this.sendConfirmation(this.currentLogEntryIndex - 1);

      notification.showMessage(
        isLogged,
        "move logged",
        "error logging to server"
      );

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
