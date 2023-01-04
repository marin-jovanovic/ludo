<template>
  <base-user-template>
    <div>order</div>

    <div v-for="(p, k) in this.players" :key="k">
      join index : {{ k }} , id: {{ p.id }} , username: {{ p.username }}, is
      their turn: {{ p.isTurn }}
    </div>
    <TheDice ref="dice"></TheDice>

    <button @click="rollDice">roll dice</button>

    <h3>performing entry: {{ this.currentLogEntryIndex }}</h3>

    <h3>order : {{ this.order }}</h3>

    <!-- <BaseNotification ref="notification"></BaseNotification> -->

    <!-- <div>order</div>

    <h1>total level capacity : {{ this.capacity }}</h1>

    <h1>users:</h1>

    <div v-for="(p, k) in this.players" :key="k">{{ k }} -> {{ p }}</div>

    <button v-if="this.canStart" enabled @click="this.startgame">start</button>
    <button v-else disabled>start</button> -->
  </base-user-template>
</template>

<script>
import TheDice from "@/components/TheDice.vue";
import BaseUserTemplate from "@/components/BaseUserTemplate.vue";

import { apiLevelLog } from "@/scripts/api/level_log";
import { apiLevel } from "@/scripts/api/level";
import { acceptanceLogApi } from "@/scripts/api/acceptance_log";
import { apiSettings } from "@/scripts/api/settings";
// import { apiLevel } from "@/scripts/api/level";

import { wsListeners } from "@/scripts/ws_listener";

import { notification } from "@/scripts/notification";

export default {
  data() {
    return {
      levelId: undefined,
      players: {},
      joinId: undefined,
      log: undefined,
      currentLogEntryIndex: undefined,
      username: undefined,
      order: [],
    };
  },

  async mounted() {
    this.levelId = this.$route.params.id;

    let url = "ws://127.0.0.1:8000/acceptanceLogEntryCreated/";
    new wsListeners.WebSocketListener(url, this.wsReceive);

    await this.loadUsername();

    await this.loadPlayers();
    await this.loadPlayingOrder();

    await this.loadConfirmationLog();

    await this.tryNextInstruction();
  },
  methods: {
    async tryNextInstruction() {
      console.log("try");
      console.log(this.currentLogEntryIndex);

      let logEntry = this.log[this.currentLogEntryIndex];

      if (logEntry.action === "goes") {
        console.log("goes");
        this.order.push(this.players[logEntry.player].username);
      } else {
        return;
      }

      this.currentLogEntryIndex++;

      await this.sendConfirmation(this.currentLogEntryIndex - 1);
    },

    // async playerJoinIndexToUsername(joinIndex) {
    //   let res = await apiLevel.getSpecificLevel({
    //     levelId: this.levelId,
    //   });

    //   let flag = res["auth"]["status"] && res["payload"]["status"];

    //   if (!flag) {
    //     console.log("err");
    //     return;
    //   }

    //   for (const i of Object.values(res["payload"]["users"])) {
    //     if (i.joinId === joinIndex) {
    //       return i.username;
    //     }
    //   }

    //   // return
    //   // return res["payload"];
    // },

    // passive actions
    async wsReceive(message) {
      console.log("received update", message);

      let toAcceptIndex = message.entryId;

      // this should be compared with >
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

      // fast loading

      for (const entry of Object.values(this.log)) {
        if (performedEntries.has(entry.id)) {
          console.log("perform", entry.id);

          switch (entry.action) {
            case "roll":
              console.log("roll");
              break;
            case "goes":
              console.log("goes");
              this.order.push(this.players[entry.player].username);
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

    async loadUsername() {
      let r = await apiSettings.getSettings();

      // fixthuis check
      if (r["auth"]["status"]) {
        let pl = r["payload"];

        this.username = pl["username"];
      }
    },

    async rollDice() {
      // todo sta ako ovaj reloada stranicu, nece sve ponovo krenut vrtit, treba samo ovo sta se nije rjesilo

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

      for (const value of Object.values(res["payload"]["users"])) {
        if (value.username === this.username) {
          this.joinId = value.joinId;
        }
      }

      for (const [key, value] of Object.entries(res["payload"]["users"])) {
        this.players[value.joinId] = {
          username: value.username,
          isTurn: false,
          id: key,
        };
      }
    },

    async loadPlayingOrder() {
      let res = await apiLevelLog.getLevelLog(this.levelId);

      if (!(res["auth"]["status"] && res["payload"]["status"])) {
        console.log("err");
        return;
      }

      this.log = res["payload"]["log"];
      console.log(res["payload"]["log"]);

      this.currentLogEntryIndex = 0;

      let logEntry = this.log[this.currentLogEntryIndex];

      this.players[logEntry.player].isTurn = true;
    },
  },

  components: {
    BaseUserTemplate,
    TheDice,
  },
};
</script>

<style>
</style>