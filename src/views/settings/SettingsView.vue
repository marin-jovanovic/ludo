<template>
  <BaseUserTemplate>
    <div class="container-fluid">
      <div class="row">
        <h1>personal info</h1>

        username
        <input v-model="this.username" placeholder="" />
        <br />
        <br />

        email
        <input v-model="this.email" placeholder="" />
        <br />
        <br />

        password
        <input v-model="this.password" placeholder="" type="password" />
        <input v-model="this.passwordConfirm" placeholder="" type="password" />
        <br />

        profile photo

        <div>
          <img v-bind:src="this.profilePhoto" />
          <br />
          <input type="file" accept="image" @change="uploadImage" />
        </div>

        <br />

        <button @click="saveChanges">save changes on profile metadata</button>
        <button>view reviews</button>

        <button @click="deleteAccount">delete account</button>

        profile picture
        <img
          :src="this.profilePhoto"
          style="width: 100px; height: 100px; border-radius: 50%"
          :alt="this.username"
        />
      </div>
    </div>
  </BaseUserTemplate>
</template>
  
<script>
import { apiSettings } from "@/scripts/api/settings";
import BaseUserTemplate from "@/components/BaseUserTemplate.vue";
import { router } from "@/router/router";
import { notification } from "@/scripts/notification";
import { userMetaSS } from "@/scripts/session_storage";

export default {
  data() {
    return {
      username: "",
      email: "",
      profilePhoto: "",
      password: "",
      passwordConfirm: "",
      passwordCurrent: "",

      originalUsername: "",
    };
  },

  watch: {
    profilePhoto(newProfilePhoto) {
      userMetaSS.updateSettings({
        changes: { userProfilePhoto: newProfilePhoto },
      });
    },
  },

  async mounted() {
    let res = await apiSettings.getSettings();

    let flag = res["auth"]["status"] && res["payload"]["status"];

    if (!flag) {
      console.log("err");
      return;
    }

    this.profilePhoto = res["payload"]["profilePhoto"];
    this.originalUsername = res["payload"]["username"];
    this.username = res["payload"]["username"];

    this.profilePhoto = userMetaSS.getUserMeta()["userProfilePhoto"];

    console.log(this.profilePhoto);

    let r = await apiSettings.getSettings();

    if (r["auth"]["status"]) {
      let pl = r["payload"];

      this.username = pl["username"];

      this.profilePhoto = pl["userProfilePhoto"];
    }
  },
  methods: {
    async deleteAccount() {
      console.log("delete acc");

      let res = await apiSettings.deleteAccount(this.originalUsername);

      notification.showMessage(
        res["auth"]["status"] && res["payload"]["status"],
        `post deleted`,
        `error deleting post`
      );

      console.log("remove from session storage user");

      this.returnUrl = "/login";
      router.push(this.returnUrl);
    },

    uploadImage(e) {
      const image = e.target.files[0];
      const reader = new FileReader();
      reader.readAsDataURL(image);
      reader.onload = (e) => {
        this.profilePhoto = e.target.result;
      };
    },

    saveChanges() {
      apiSettings.updateSettings({
        username: this.username,
        email: this.email,
        profilePhoto: this.profilePhoto,
      });
    },
  },
  components: { BaseUserTemplate },
};
</script>
  
<style>
</style>