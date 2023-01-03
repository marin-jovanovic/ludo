<template>
  <base-user-template>
    <div>order</div>

    <div v-for="(p, k) in this.players" :key="k">
      join index : {{ k }} , id: {{ p.id }} , username: {{ p.username }}, is
      their turn: {{ p.isTurn }}
    </div>
    <TheDice ref="dice"></TheDice>

    <button @click="rollDice">roll dice</button>

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
import { apiLevelLog } from "@/scripts/api/level_log";
import { apiLevel } from "@/scripts/api/level";
import { acceptanceLogApi } from "@/scripts/api/acceptance_log";
import TheDice from "@/components/TheDice.vue";
import { apiSettings } from "@/scripts/api/settings";

import BaseUserTemplate from "@/components/BaseUserTemplate.vue";

export default {
  data() {
    return {
      levelId: undefined,
      players: {},
      joinId: undefined,
      log: undefined,
      currentLogEntryIndex: undefined,
      username: undefined,
    };
  },

  async mounted() {
    this.levelId = this.$route.params.id;

    await this.loadUsername();

    await this.loadPlayers();
    await this.loadPlayingOrder();
  },
  methods: {
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

      if (logEntry.player !== this.joinId) {
        console.log("err: internal, not your turn");
        return;
      }

      if (logEntry.action !== "roll") {
        console.log("not roll action");
        return;
      }

      this.$refs.dice.rollDice(logEntry.diceResult);

      // send to backend that it is performed
      let res = await acceptanceLogApi.addEntryToAcceptanceLog({
        levelId: this.levelId,
        entryId: this.currentLogEntryIndex,
      });

      if (!(res["auth"]["status"] && res["payload"]["status"])) {
        console.log("err");
        return;
      }

      console.log(res["payload"]);

      if (!res["payload"]["status"]) {
        console.log("err ??");
      }

      //   cleanup
      this.players[this.joinId].isTurn = false;

      // safe increment
      this.currentLogEntryIndex++;
      logEntry = this.log[this.currentLogEntryIndex];
      this.players[logEntry.player].isTurn = true;

      console.log("now is (join index)", logEntry.player, "turn");

      // add notif that move is logged on BE

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
        console.log(value.username, this.username);

        if (value.username === this.username) {
          this.joinId = value.joinId;
        }
      }

      for (const [key, value] of Object.entries(res["payload"]["users"])) {
        console.log(key, value);

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

      this.currentLogEntryIndex = 0;

      let logEntry = this.log[this.currentLogEntryIndex];

      //   console.log("current", logEntry);

      //   console.log(logEntry.player, this.joinId);

      //   if (logEntry.player !== this.joinId) {
      //     console.log("not your turn");
      //     return;
      //   }

      this.players[logEntry.player].isTurn = true;
    },

    // setTurn(userId) {
    //   for (const [key, value] of Object.entries(this.players)) {
    //     console.log(key, value);

    //     this.players[key] = {
    //       username: value.username,
    //       isTurn: false,
    //     };
    //   }

    //   this.players[userId].isTurn = true;
    // },
  },

  components: {
    BaseUserTemplate,
    TheDice,
  },
};
</script>

<style>
</style>