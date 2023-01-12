<template>
  <base-user-template>
    <div>
      <div class="container">
        <div class="left-div" style="width: 5%; float: left"></div>
        <div
          class="middle-div"
          style="width: 90%; float: left; border: 1px solid"
        >
          <slot />
        </div>
        <div class="right-div" style="width: 5%; float: left"></div>
      </div>
    </div>

    <!-- <base-middle-container> -->

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
            <div class="message message-sent">
              <p class="message-text">Hello, how are you?</p>
              <p class="message-timestamp">12:34 PM</p>
            </div>
            <div class="message message-received">
              <p class="message-text">
                I'm good, thanks for asking! How about you?
              </p>
              <p class="message-timestamp">1:00 PM</p>
            </div>
          </div>
          <form>
            <input type="text" placeholder="Enter message here" />
            <button type="submit">Send</button>
          </form>
        </div>
      </div>
    </div>
    <!-- </base-middle-container> -->
  </base-user-template>
</template>
      
    <script>
import BaseUserTemplate from "@/components/BaseUserTemplate.vue";
import { userConnectionApi } from "@/scripts/api/user_connection";
// import BaseMiddleContainer from "@/components/BaseMiddleContainer.vue";

import { f } from "@/scripts/diffe_helman";

export default {
  data() {
    return {
      username: undefined,
      profilePhoto: undefined,
      openDrawer: true,
      userConnections: undefined,

      activeConversation: undefined,
    };
  },

  async mounted() {
    let userId = this.$route.params.userId;
    console.log("user id", userId);

    f();

    let r = await userConnectionApi.getAllConnections();
    console.log(r);
    this.userConnections = r["userConnections"];
  },
  methods: {
    async createChatRoom() {
      let r = await userConnectionApi.getAllConnections();
      console.log(r);
    },
  },
  components: {
    BaseUserTemplate,
    // BaseMiddleContainer,
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
