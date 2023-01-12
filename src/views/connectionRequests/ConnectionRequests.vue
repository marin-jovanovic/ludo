<template>
  <base-user-template>
    <div>
      <div class="container">
        <div class="left-div" style="width: 15%; float: left"></div>
        <div class="middle-div" style="width: 70%; float: left"></div>
        <div class="right-div" style="width: 15%; float: left"></div>
      </div>
    </div>
  </base-user-template>
</template>
          
        <script>
import BaseUserTemplate from "@/components/BaseUserTemplate.vue";
import { userConnectionApi } from "@/scripts/api/user_connection";
import { userApi } from "@/scripts/api/user";
import { userProfilePhoto } from "@/scripts/api/user_profile_photo";

export default {
  data() {
    return {
      users: [],
      currentPage: 0,
      icon1: {
        on: "chat_bubble",
        off: "chat_bubble_outline",
      },
      icon2: {
        on: "add_circle",
        off: "add_circle_outline",
      },
      icon3: {
        on: "remove_circle",
        off: "remove_circle_outline",
      },
    };
  },
  async mounted() {
    await this.fetchUsers();
  },
  methods: {
    async addUser(userId) {
      console.log("add user", userId);

      let r = userConnectionApi.sendConnectionRequest({ userId: userId });
      console.log(r);
    },

    async fetchUsers() {
      let t = await userApi.getAllUsers();
      console.log(t);

      this.users = t.users;

      for (const [userId, userMeta] of Object.entries(this.users)) {
        console.log(userId, userMeta);

        let r = await userProfilePhoto.getProfilePhoto({ userId: userId });

        this.users[userId]["userProfilePhoto"] = r["userProfilePhoto"];
      }
    },
    async fetchMoreUsers() {
      this.fetchUsers();
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

.demo-card--photo {
  width: 200px;
}

.demo-card__media {
  /* background-image: url("images/1-1.jpg"); */
}

.demo-card__media-content--with-title {
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
}

.demo-card__media-title {
  padding: 8px 16px;
  background-image: linear-gradient(
    to bottom,
    rgba(0, 0, 0, 0) 0%,
    rgba(0, 0, 0, 0.5) 100%
  );
  color: white;
}
</style>  
    