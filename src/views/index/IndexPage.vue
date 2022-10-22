<template>
  <BaseUserTemplate>
    <input
      type="text"
      class="form-control"
      placeholder="game name"
      v-model="gameName"
    />
    <input
      type="text"
      class="form-control"
      placeholder="game capacity"
      v-model="gameCapacity"
    />

    <button @click="createGame">create game</button>

    <hr />
    <h1>not full</h1>
    <hr />

    <div v-for="i in this.notFull" :key="i">
      {{ i }}

      <button @click="joinGame(i.name)">join</button>

      <div v-for="p in i.players" :key="p">
        <div v-if="p == this.username">
          <h1>here</h1>
          <button @click="leaveGame(i.name)">leave</button>
        </div>
      </div>

      <hr />
    </div>

    <hr />
    <h1>full</h1>
    <hr />

    <div v-for="i in this.full" :key="i">
      {{ i }}
      <div v-for="p in i.players" :key="p">
        <div v-if="p == this.username">
          <h1>here</h1>
          <button @click="leaveGame(i.name)">leave</button>

          <!-- <button @click="leaveGame(i.name)">start</button> -->
        </div>
      </div>

      <hr />
    </div>

    <BaseMessage ref="message"></BaseMessage>
  </BaseUserTemplate>
</template>

<script>
import { useToast } from "vue-toastification";
import BaseUserTemplate from "@/components/BaseUserTemplate.vue";
import BaseMessage from "@/components/BaseMessage.vue";
import { apiLobby } from "@/scripts/api/lobby";
// import BasePortfolioList from "@/components/BasePortfolioList.vue";
import { wsListeners } from "@/scripts/ws_listener";
import { router } from "@/router/router";

export default {
  setup() {
    const toast = useToast();
    return { toast };
  },

  async mounted() {
    this.username = sessionStorage.getItem("username");

    await this.fetchInitData();

    let url = "ws://127.0.0.1:8000/whole1/";
    new wsListeners.WebSocketListener(url, this.getUserActive);
    console.log("ws init");
  },
  data() {
    return {
      gameName: "",
      gameCapacity: "",

      full: {},
      notFull: {},

      username: "",
    };
  },
  methods: {
    getUserActive(message) {
      console.log("ws get user active");
      console.log(message);
      this.fetchInitData();
    },

    async joinGame(gameName) {
      let res = await apiLobby.joinGame(gameName);
      console.log("load", res);
      if (res["auth"]["status"]) {
        if (res["payload"]["status"]) {
          console.log("game join ok");
        }
      }
    },

    async leaveGame(gameName) {
      let res = await apiLobby.leaveGame(gameName);
      console.log("load", res);
      if (res["auth"]["status"]) {
        if (res["payload"]["status"]) {
          console.log("game left ok");
        }
      }
    },
    async createGame() {
      let res = await apiLobby.createGame(this.gameName, this.gameCapacity);
      console.log("load", res);
      if (res["auth"]["status"]) {
        if (res["payload"]["status"]) {
          console.log("game created ok");
        }
      }
    },

    async fetchInitData() {
      let res = await apiLobby.getGames();
      console.log(res);
      if (res["auth"]["status"]) {
        res["payload"]["payload"]["full"].forEach((i) => {
          console.log(i);

          i.players.forEach((j) => {
            if (j == this.username) {
              console.log("start game");

              sessionStorage.setItem("gameId", i.name);

              router.push("game");
            }
          });
        });

        this.full = res["payload"]["payload"]["full"];
        this.notFull = res["payload"]["payload"]["not full"];
      } else {
        console.log("err fetching data");
      }
    },
  },
  components: {
    BaseUserTemplate,

    BaseMessage,
  },
};
</script>
