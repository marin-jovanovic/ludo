<template>
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
</template>
    
    
  <script>
import { wsListeners } from "@/scripts/ws_listener";
import { apiMessage } from "@/scripts/api/message";

export default {
  data() {
    return { username: "", gameId: "", message: "", messageLog: {} };
  },
  async mounted() {
    this.gameId = sessionStorage.getItem("gameId");
    this.username = sessionStorage.getItem("username");

    await this.fetchMessages();

    let url = "ws://127.0.0.1:8000/msg/";
    new wsListeners.WebSocketListener(url, this.newMsg);
  },
  methods: {
    newMsg(message) {
      this.messageLog.push(message);
    },

    async sendMessage() {
      let res = await apiMessage.sendMessage(
        this.username,
        this.gameId,
        this.message
      );
      if (res["auth"]["status"]) {
        console.log(res);
      } else {
        console.log("err fetching data");
      }
    },

    async fetchMessages() {
      let res = await apiMessage.getMessages(this.gameId);
      if (res["auth"]["status"]) {
        this.messageLog = res["payload"]["payload"];
      } else {
        console.log("err fetching data");
      }
    },
  },
};
</script> 
    
