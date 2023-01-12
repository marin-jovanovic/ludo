<template>
  <base-user-template>
    <div class="container">
      <div class="header">
        <h1>Messaging App</h1>
        <div class="header-right">
          <button id="new-group-btn">New Group</button>
          <a href="#">Settings</a>
        </div>
      </div>
      <div class="split-screen">
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
  </base-user-template>
</template>
      
    <script>
import BaseUserTemplate from "@/components/BaseUserTemplate.vue";
import { userConnectionApi } from "@/scripts/api/user_connection";

export default {
  data() {
    return {
      username: undefined,
      profilePhoto: undefined,
      openDrawer: true,
      userConnections: undefined,
    };
  },
  async mounted() {
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
  },
};
</script>
 



<style>
.container {
  width: 80%;
  margin: 0 auto;
}
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  background-color: #0088cc;
  color: #fff;
}
.header-right a {
  margin-left: 10px;
  color: #fff;
  text-decoration: none;
}
.conversation-list {
  height: 300px;
  overflow-y: scroll;
}
.conversation {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  border-bottom: 1px solid #ccc;
}
.conversation-info {
  display: flex;
  align-items: center;
}

.conversation-timestamp {
  font-size: 12px;
  color: #999;
}
.conversation-view {
  border: 1px solid #ccc;
  padding: 10px;
  margin-top: 10px;
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
  width: 20%;
  height: 300px;
  overflow-y: scroll;
}
.conversation-view {
  width: 80%;
}
</style>
