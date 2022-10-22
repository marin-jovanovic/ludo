<template>
  <BaseUserTemplate>
    <!-- <hr /> -->
    <br />

    <h1>now playing:</h1>

    <div class="row">
      <div class="col"></div>
      <div class="col">
        <TheDice ref="dice"></TheDice>
      </div>
      <div class="col">
        <button @click="rollDice">roll dice</button>
      </div>
    </div>

    <div>
      <div>messages</div>

      <div>
        <div v-for="i in this.messageLog" :key="i">
          {{ i }}
        </div>
      </div>
      <div>
        <input type="text" v-model="this.message" placeholder="type message" />
        <button @click="sendMessage">send</button>
      </div>
    </div>

    <div class="row"></div>
  </BaseUserTemplate>
</template>


<script>
import TheDice from "./TheDice.vue";
import BaseUserTemplate from "@/components/BaseUserTemplate.vue";
import { apiMessage } from "@/scripts/api/message";
import { wsListeners } from "@/scripts/ws_listener";

export default {
  data() {
    return {
      canRoll: true,
      message: "",
      username: "",
      gameId: "",

      messageLog: {},
    };
  },
  async mounted() {
    this.username = sessionStorage.getItem("username");
    this.gameId = sessionStorage.getItem("gameId");
    await this.fetchMessages();

    let url = "ws://127.0.0.1:8000/msg/";
    new wsListeners.WebSocketListener(url, this.newMsg);
    console.log("ws init");
  },
  methods: {
    newMsg(message) {
      console.log("ws newmsg");
      console.log(message);
      console.log(typeof message);

      this.messageLog.push(message);
      //   this.fetchInitData();
    },

    async sendMessage() {
      console.log("send msg", this.message);

      let res = await apiMessage.sendMessage(
        this.username,
        this.gameId,
        this.message
      );
      console.log(res);
      if (res["auth"]["status"]) {
        console.log(res);

        // console.log(res["payload"])

        // res["payload"]["payload"]["full"].forEach((i) => {
        //   i.players.forEach((j) => {
        //     if (j == this.username) {
        //       console.log("start game");
        //       router.push("game");
        //     }
        //   });
        // });
      } else {
        console.log("err fetching data");
      }
    },

    async fetchMessages() {
      console.log("get messages");
      let res = await apiMessage.getMessages(this.gameId);
      console.log(res);
      if (res["auth"]["status"]) {
        console.log(res);

        console.log(res["payload"]["payload"]);
        this.messageLog = res["payload"]["payload"];

        // console.log(res["payload"])

        // res["payload"]["payload"]["full"].forEach((i) => {
        //   i.players.forEach((j) => {
        //     if (j == this.username) {
        //       console.log("start game");
        //       router.push("game");
        //     }
        //   });
        // });
      } else {
        console.log("err fetching data");
      }
    },

    rollDice() {
      if (!this.canRoll) {
        return;
      }

      this.$refs.dice.rollDice(5);
    },
  },
  components: { TheDice, BaseUserTemplate },
};
</script> 

<style>
.col {
  border: 1mm solid black;
}
</style>