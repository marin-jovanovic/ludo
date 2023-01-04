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
// import { useToast } from "vue-toastification";
import BaseNotification from "@/components/BaseNotification.vue";
import { router } from "@/router/router";

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
  // setup() {
  //   const toast = useToast();
  //   return { toast };
  // },
  async mounted() {
    this.gameId = this.$route.params.id;
    console.log(this.gameId);

    // this needs to be same as one in sesion storage

    // fetch users here

    let res = await apiLevel.getSpecificLevel({ levelId: this.gameId });
    console.log("load", res);
    if (res["auth"]["status"]) {
      if (res["payload"]["status"]) {
        console.log(res["payload"]);

        this.players = res["payload"]["users"];
        this.capacity = res["payload"]["capacity"];

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
      }
    }

    this.canStart = Object.keys(this.players).length === this.capacity;
  },
  methods: {
    startgame() {
      //   sessionStorage.setItem("gameId", inGame);

      // router.push(`/game/${this.gameId}`);

      router.replace(`/game/${this.gameId}`);
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
