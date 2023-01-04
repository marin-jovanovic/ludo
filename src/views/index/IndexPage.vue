<template>
  <BaseUserTemplate>
    <div class="row">
      <input
        type="text"
        class="form-control"
        placeholder="game name"
        v-model="gameName"
      />
      <input
        type="number"
        class="form-control"
        placeholder="game capacity"
        v-model="gameCapacity"
      />

      <button @click="createGame">create game</button>
    </div>

    <hr />

    <div v-for="i in this.levels" :key="Object.values(i)">
      {{ i }}

      <button @click="joinGame(i.levelId)">join</button>

      <div v-for="p in i.players" :key="p">
        <div v-if="p == this.username">
          <h1>here</h1>
          <button @click="leaveGame(i.levelId)">leave</button>
        </div>
      </div>

      <hr />
    </div>

    <div>
      active users:
      <div v-for="(user, id) in this.activeUsers" :key="id">
        {{ id }} --> {{ user }}
      </div>
    </div>
  </BaseUserTemplate>
</template>

<script>
import BaseUserTemplate from "@/components/BaseUserTemplate.vue";
import { apiLevel } from "@/scripts/api/level";
import { wsListeners } from "@/scripts/ws_listener";
import { router } from "@/router/router";
import { levelSessionStorage, userMetaSS } from "@/scripts/session_storage";
import { notification } from "@/scripts/notification";

export default {
  async mounted() {
    this.username = userMetaSS.getCredentials()["username"];

    await this.fetchInitData();

    let url = "ws://127.0.0.1:8000/lobby_games/";
    new wsListeners.WebSocketListener(url, this.getUserActive);
  },
  data() {
    return {
      gameName: "",
      gameCapacity: 2,

      levels: {},

      username: "",

      isCreator: false,
      canStart: false,

      activeUsers: {},
    };
  },
  methods: {
    getUserActive(message) {
      console.log("ws get user active");
      console.log(message);

      this.activeUsers = message["payload"];
      this.fetchInitData();
    },

    async joinGame(levelId) {
      let res = await apiLevel.joinGame(levelId);

      let flag = res["auth"]["status"] && res["payload"]["status"];

      notification.showMessage(flag, "joined level", "error joining level");

      if (!flag) {
        return;
      }

      // let levelId = res["payload"]["levelId"];

      // console.log("join pl", res["payload"]);
      console.log("level id", levelId);

      if (levelId !== Number(res["payload"]["levelId"])) {
        console.log("err not same", res["payload"]);
      }

      // cons

      levelSessionStorage.joinLevel({ levelId: levelId });

      router.push(`waitingRoom/${levelId}`);
    },

    async leaveGame(gameName) {
      let res = await apiLevel.leaveGame(gameName);

      let flag = res["auth"]["status"] && res["payload"]["status"];

      notification.showMessage(flag, "leave ok", "error level leave");

      if (!flag) {
        return;
      }

      levelSessionStorage.leaveLevel();
    },

    async createGame() {
      let res = await apiLevel.createGame(this.gameName, this.gameCapacity);
      console.log("load", res["payload"]);

      let flag = res["auth"]["status"] && res["payload"]["status"];

      notification.showMessage(flag, "level created", "error creating level");

      if (!flag) {
        return;
      }

      this.isCreator = true;

      let levelId = res["payload"]["levelId"];

      this.joinGame(levelId);

      // todo wait 2 seconds or something?
      // better: trigger notif

      levelSessionStorage.joinLevel({ levelId: res["payload"]["levelId"] });

      router.push(`waitingRoom/${levelId}`);
    },

    async fetchInitData() {
      let res = await apiLevel.getGames();
      if (!res["auth"]["status"]) {
        console.log("err fetching data");
        return;
      }

      console.log(res[["payload"]]);

      this.levels = res["payload"]["levels"];
      console.log(res["payload"]["levels"]);

      let inGame = res["payload"]["inLevel"];

      console.log("in game", inGame);
    },
  },
  components: {
    BaseUserTemplate,
  },
};
</script>
