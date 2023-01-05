<template>
  <div>
    <button @click="openDrawer = 'right'">show messages</button>

    <w-drawer v-model="openDrawer" :right="true">
      <div class="w-flex pa2 align-center wrap">
        <!-- for offset from navigation header -->
        <div style="max-height: 20%"></div>

        <div
          style="border-style: solid"
          class="content scrollable"
          ref="msgContainer"
        >
          <div v-for="i in this.messageLog" :key="i">
            <!-- <div style="border-style: solid"> -->
            <div>
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
          </div>
        </div>

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
  max-height: 80%;
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

export default {
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

    await this.fetchMessages();

    let url = "ws://127.0.0.1:8000/msg/";
    new wsListeners.WebSocketListener(url, this.newMsg);

    this.scrollToBottom();
  },

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

      // triggered on new msg from ws, no need to call
      // await this.scrollToBottom();
    },

    async scrollToBottom() {
      this.$nextTick(() => {
        var container = this.$refs.msgContainer;

        if (container) {
          container.scrollTop = container.scrollHeight + 200;
        }
      });
    },

    async fetchMessages() {
      let res = await apiMessage.getMessages(this.levelId);

      let flag = res["auth"]["status"] && res["payload"]["status"];

      if (!flag) {
        console.log("err");
      }

      this.messageLog = res["payload"]["payload"];

      await this.scrollToBottom();
    },
  },
};
</script> 
    
