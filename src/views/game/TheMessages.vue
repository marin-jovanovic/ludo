<template>
  <div>
    <w-button class="ma1" @click="openDrawer = 'right'" outline>
      Open right drawer
    </w-button>

    <w-drawer v-model="openDrawer" :right="true">
      <!-- todo css -->

      <!-- <w-button
        @click="openDrawer = false"
        sm
        outline
        round
        absolute
        icon="wi-cross"
      >
        fff

        <h1>f</h1>
        <h1>f</h1>
        <h1>f</h1>
        <h1>f</h1>
        <h1>f</h1>
        <h1>f</h1>
        <h1>f</h1>
      </w-button> -->

      <div class="w-flex pa2 align-center wrap">
        <div class="w-flex align-center">
          <!-- <span class="grey-dark3"> fff </span> -->

          <!-- <div>messages</div> -->
          <div class="column">
            <div class="row">
              <div
                ref="messagesScrollable"
                style="overflow-y: scroll; height: 400px"
              >
                <div v-for="i in this.messageLog" :key="i">
                  {{ i }}
                </div>
              </div>
            </div>
            <div class="row">
              <input
                type="text"
                v-model="this.message"
                placeholder="type message"
              />
              <button @click="sendMessage">send</button>
            </div>
          </div>
        </div>
      </div>
    </w-drawer>
  </div>
</template>


    
    
  <script>
import { wsListeners } from "@/scripts/ws_listener";
import { apiMessage } from "@/scripts/api/message";
import { levelSessionStorage, userMetaSS } from "@/scripts/session_storage";

export default {
  props: {},
  // computed: {
  //   position() {
  //     return "right";
  //   },
  // },
  updated() {
    var elem = this.$el;
    elem.scrollTop = elem.clientHeight;
  },
  data() {
    return {
      levelId: "",

      username: "",
      message: "",
      messageLog: {},
      openDrawer: false,
    };
  },
  async mounted() {
    this.levelId = levelSessionStorage.getLevelMeta()["levelId"];

    this.username = userMetaSS.getCredentials()["username"];

    // userMetaSS,
    // levelSessionStorage

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
        this.levelId,
        this.message
      );
      if (res["auth"]["status"]) {
        console.log(res);
      } else {
        console.log("err fetching data");
      }

      // let el = this.$refs.messagesScrollable;

      // el.scrollIntoView({ behavior: "smooth" });

      var container = this.$el.querySelector(
        ".column > div:nth-child(1) > div:nth-child(1)"
      );
      container.scrollTop = container.scrollHeight;

      this.message = "";
    },

    async fetchMessages() {
      let res = await apiMessage.getMessages(this.levelId);

      let flag = res["auth"]["status"] && res["payload"]["status"];

      if (!flag) {
        console.log("err");
      }

      console.log(res["payload"]);

      this.messageLog = res["payload"]["payload"];

      // if (res["auth"]["status"]) {
      // } else {
      //   console.log("err fetching data");
      // }
    },
  },
};
</script> 
    
