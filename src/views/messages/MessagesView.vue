<template>
  <base-user-template>
    <div>
      <div class="container">
        <div class="left-div" style="width: 5%; float: left"></div>
        <div
          class="middle-div"
          style="width: 90%; float: left; border: 1px solid"
        ></div>
        <div class="right-div" style="width: 5%; float: left"></div>
      </div>
    </div>

    <hr />
    <br />
    <div style="display: flex">
      <div style="width: 30%">
        <div class="conversation-list" id="conversation-list-scrollable">
          <form>
            <input
              type="text"
              id="search-input"
              placeholder="Search conversations"
            />
          </form>
          <div class="conversation" v-for="i in this.userConnections" :key="i">
            <img :src="i.profilePhoto" alt="Profile Picture" />
            <div class="conversation-info">
              <div class="conversation-name">{{ i.username }}</div>
              <div class="conversation-preview">
                {{ i.lastMessageContent }}
              </div>
            </div>
          </div>
        </div>
      </div>
      <div style="width: 70%">
        <div class="conversation-view">
          <div class="message-list">
            <div v-for="(message, index) in this.messages" :key="index">
              <div
                v-if="Number(message.senderId) === Number(this.userId)"
                class="message message-received"
              >
                <p class="message-text">
                  {{ message.content }}
                </p>
                <p class="message-timestamp">
                  {{ message.timestamp }}
                </p>
              </div>

              <div class="message message-sent" v-else>
                <p class="message-text">{{ message.content }}</p>
                <p class="message-timestamp">
                  {{ message.timestamp }}
                </p>
              </div>
            </div>
          </div>
          <input
            type="text"
            v-model="message"
            placeholder="Enter message here"
          />
          <button @click="sendMessage">Send</button>
        </div>
      </div>
    </div>
  </base-user-template>
</template>
      
    <script>
import BaseUserTemplate from "@/components/BaseUserTemplate.vue";
import { userConnectionApi } from "@/scripts/api/user_connection";
import { directMessagesApi } from "@/scripts/api/direct_messages";

export default {
  data() {
    return {
      username: undefined,
      profilePhoto: undefined,
      openDrawer: true,
      userConnections: undefined,

      activeConversation: undefined,

      message: "",
      userId: undefined,
      messages: undefined,
    };
  },

  async mounted() {
    this.userId = this.$route.params.userId;
    console.log("user id", this.userId);

    let messages = await directMessagesApi.getMessages(this.userId);

    console.log("messages");
    console.log(messages);

    this.messages = messages.messages;

    let r = await userConnectionApi.getAllConnections();
    console.log(r);
    this.userConnections = r["userConnections"];
  },
  methods: {
    async createChatRoom() {
      let r = await userConnectionApi.getAllConnections();
      console.log(r);
    },
    async sendMessage() {
      console.log("send", this.message);

      let messages = await directMessagesApi.sendMessage({
        userId: this.userId,
        content: this.message,
      });

      console.log(messages);

      this.message = "";
    },
  },
  components: {
    BaseUserTemplate,
  },
};
</script>
 



<style>
.container {
  display: flex;
  justify-content: space-between;
}
.left-div,
.middle-div,
.right-div {
  height: 100%;
}

.conversation-timestamp {
  font-size: 12px;
  color: #999;
}

.message-list {
  height: 300px;
  overflow-y: scroll;
}
.message {
  margin-bottom: 10px;
}
.message-sent {
  text-align: right;
}
.message-received {
  text-align: left;
}
.message-text {
  padding: 10px;
  background-color: #f0f0f0;
  border-radius: 5px;
  display: inline-block;
}
.message-timestamp {
  font-size: 12px;
  color: rgb(31, 29, 29);
}

#new-group-btn {
  background-color: #0088cc;
  color: #fff;
  padding: 5px 10px;
  border: none;
  border-radius: 5px;
}
#conversation-list-scrollable {
  height: 300px;
  overflow-y: scroll;
}
.conversation {
  display: flex;
  align-items: center;
  padding: 10px;
  border-bottom: 1px solid #ccc;
}
.conversation img {
  width: 50px;
  height: 50px;
  border-radius: 25px;
  margin-right: 10px;
}
.conversation-info {
  display: flex;
  flex-direction: column;
}
.conversation-name {
  font-weight: bold;
  margin-bottom: 5px;
}
.conversation-preview {
  color: rgb(3, 3, 3);
  font-size: 12px;
}
.split-screen {
  display: flex;
}
.conversation-list {
  height: 300px;
  overflow-y: scroll;
}
.conversation-view {
  width: 80%;
}
</style>
