<template>
  <base-user-template>
    <BaseNotification ref="notification"></BaseNotification>

    <div>waiting room level</div>

    <h1>total level capacity : {{ this.capacity }}</h1>

    <h1>users:</h1>

    <div v-for="(p, k) in this.players" :key="k">{{ k }} -> {{ p }}</div>

    <button v-if="this.canStart" enabled @click="this.startgame">start</button>
    <button v-else disabled>start</button>
  </base-user-template>
</template>

<script>
import BaseUserTemplate from "@/components/BaseUserTemplate.vue";
import { apiLevel } from "@/scripts/api/level";
import BaseNotification from "@/components/BaseNotification.vue";
import { router } from "@/router/router";
import { wsListeners } from "@/scripts/ws_listener";

export default {
  components: { BaseUserTemplate, BaseNotification },
  data() {
    return {
      gameId: undefined,
      players: undefined,
      capacity: undefined,
      canStart: false,
    };
  },
  async mounted() {
    let url = "ws://" + process.env.VUE_APP_BACKEND_WS + "/joinLeft/";
    new wsListeners.WebSocketListener(url, this.wsReceive);

    console.log(url);

    this.gameId = this.$route.params.id;

    // this needs to be same as one in sesion storage

    // fetch users here
    await this.fetchUsers();
  },
  methods: {
    async wsReceive(message) {
      console.log("received update", message);

      await this.fetchUsers();
    },

    async fetchUsers() {
      let res = await apiLevel.getSpecificLevel({ levelId: this.gameId });
      console.log("load", res);

      console.log(res["payload"]);

      this.players = res["users"];
      this.capacity = res["capacity"];

      if (Object.keys(this.players).length === this.capacity) {
        console.log("level can start");
      } else {
        console.log(
          "waiting for ",
          this.capacity - Object.keys(this.players).length
        );
      }

      this.showMessage(
        Object.keys(this.players).length === this.capacity,
        "level can start",
        "waiting for " + this.capacity - Object.keys(this.players).length
      );

      // this.isCreator = true;

      // console.log("game created ok");

      // this.joinGame(this.gameName);

      // let levelId = res["payload"]["levelId"];

      // todo wait 2 seconds or something?
      // better: trigger notif

      // router.push(`waitingRoom/${levelId}`);

      this.canStart = Object.keys(this.players).length === this.capacity;
    },

    startgame() {
      router.replace(`/playingOrder/${this.gameId}`);

      // router.push(`/game/${this.gameId}`);

      // router.replace(`/game/${this.gameId}`);
      // router.replace({path: "/results/xxxx"});
    },

    showMessage(test, success, fail) {
      this.$refs.notification.showMessage(test, success, fail);
    },
  },
};
</script>

<style>
</style>
