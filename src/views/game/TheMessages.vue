<template>
  <div>
    <w-button class="ma1" @click="openDrawer = 'right'" outline>
      Open right drawer
    </w-button>

    <w-drawer v-model="openDrawer" :right="true">
      <div class="w-flex pa2 align-center wrap">
        <!-- temporary fix for offset -->
        <div class="">
          <input
            type="text"
            v-model="this.message"
            placeholder="type message"
          />
          <button @click="sendMessage">send</button>
        </div>

        <div id="container" style="max-height: 200px; overflow-y: auto">
          <!-- <ul>
            <li v-for="item in items">{{ item }}</li>
          </ul> -->
        </div>

        <div
          style="border-style: solid"
          class="content scrollable"
          ref="msgContainer"
        >
          <!-- content -->
          <ul
            v-for="(item, index) in messageLog"
            :key="index"
            :class="`index-${index}`"
          >
            <li>{{ index }} -> {{ item.content }}</li>
          </ul>
        </div>

        <!-- <div v-for="i in this.messageLog" :key="i">
            <div style="border-style: solid">
              <ui-card>
                <ui-card-content class="">
                  <div class="c">
                    <ui-card-media square class="media f"></ui-card-media>
                    <div>
                      <div>
                        <h5>
                          {{ i.sender }}
                        </h5>
                      </div>

                      <div>
                        {{ i.timestamp }}
                      </div>
                    </div>
                  </div>
                </ui-card-content>
                <ui-list-divider></ui-list-divider>
                <ui-card-actions>
                  <ui-card-buttons> {{ i }} {{ i.content }} </ui-card-buttons>
                </ui-card-actions>
              </ui-card>
            </div>
            <br />
          </div>-->

        <!-- <div ref="messagesScrollable" style="overflow-y: scroll; height: 80%">
          <ul
            v-for="(item, index) in messageLog"
            :key="index"
            :class="`index-${index}`"
          >
            <li>{{ index }} -> {{ item.content }}</li>
          </ul>
        </div> -->
        <div class="">
          <input
            type="text"
            v-model="this.message"
            placeholder="type message"
          />
          <button @click="sendMessage">send</button>
        </div>
      </div>
    </w-drawer>
  </div>
</template>




<style>
.media {
  background-color: red;
}

.c {
  display: flex;
}

.f {
  width: 110px;
}

.scrollable {
  overflow: hidden;
  overflow-y: scroll;
  max-height: 200px;
  /* height: calc(100vh - 20px); */
}
</style>
    
    
  <script>
/**
 *
 * when new message is sent from this user scroll down
 *
 * add flag to set if scrolling down on enter or keep at where is message
 *
 * add button for going to latest msg
 *
 */

import { wsListeners } from "@/scripts/ws_listener";
import { apiMessage } from "@/scripts/api/message";
import { levelSessionStorage, userMetaSS } from "@/scripts/session_storage";
// import { sleep } from "@/scripts/comm";

export default {
  props: {},
  // computed: {
  //   position() {
  //     return "right";
  //   },
  // },
  // updated() {
  // var elem = this.$el;
  // elem.scrollTop = elem.clientHeight;
  // },
  data() {
    return {
      levelId: "",

      username: "",
      message: "",
      messageLog: {},
      openDrawer: true,
    };
  },
  async mounted() {
    this.levelId = levelSessionStorage.getLevelMeta()["levelId"];

    this.username = userMetaSS.getCredentials()["username"];

    await this.fetchMessages();

    let url = "ws://127.0.0.1:8000/msg/";
    new wsListeners.WebSocketListener(url, this.newMsg);

    this.scrollToBottom();
  },

  // watch: {
  //   messageLog() {
  //     console.log("watch ");

  //     this.$nextTick(() => {
  //       console.log("scroll to bottom new");

  //       var container = this.$refs.msgContainer;
  //       container.scrollTop = container.scrollHeight + 200;
  //     });
  //   },
  // },

  // updated() {
  //   this.scrollToBottom();
  // },
  // watch: {
  //   messageLog() {
  //     console.log("watch");

  //   },
  // },

  methods: {
    async newMsg(message) {
      this.messageLog.push(message);
      await this.scrollToBottom();
    },

    async sendMessage() {
      let res = await apiMessage.sendMessage(
        this.username,
        this.levelId,
        this.message
      );

      let flag = res["auth"]["status"] && res["payload"]["status"];

      if (!flag) {
        console.log("err");
      }

      this.message = "";
      // await this.scrollToBottom();
    },

    async scrollToBottom() {
      console.log("scroll to bottom");

      this.$nextTick(() => {
        console.log("scroll to bottom new from old");

        var container = this.$refs.msgContainer;
        container.scrollTop = container.scrollHeight + 200;
      });

      // let el = this.$refs.messagesScrollable;

      // // await sleep(100);

      // // this.$refs.messagesScrollable.scrollTop =
      // //   this.$refs.messagesScrollable.scrollHeight;

      // console.log(el.scrollTop);
      // console.log(el.scrollHeight);

      // // el.scrollIntoView(true);

      // if (el) {
      //   // el.scrollTop = el.scrollHeight;
      //   el.scrollIntoView({ behavior: "smooth" });
      //   console.log("scroll performed");
      // } else {
      //   console.log("can not scroll now");
      // }

      // var container = this.$el.querySelector("#container");
      // container.scrollTop = container.scrollHeight;

      // let index = this.messageLog.length - 1;

      // // console.log(index);

      // // console.log(this.messageLog);

      // const el = this.$el.getElementsByClassName("index-" + String(index))[0];

      // console.log(el);

      // console.log();

      // if (el) {
      //   el.scrollIntoView({ behavior: "smooth" });
      // }

      // // let elmnt = el;
      // // let elmnt = document.getElementById('top');
      // elmnt.scrollIntoView(false);

      // this.$refs.messagesScrollable.scrollTop =
      //   this.$el.lastElementChild.offsetTop;
    },

    async fetchMessages() {
      let res = await apiMessage.getMessages(this.levelId);

      let flag = res["auth"]["status"] && res["payload"]["status"];

      if (!flag) {
        console.log("err");
      }

      console.log(res["payload"]);

      this.messageLog = res["payload"]["payload"];

      await this.scrollToBottom();
    },
  },
};
</script> 
    
