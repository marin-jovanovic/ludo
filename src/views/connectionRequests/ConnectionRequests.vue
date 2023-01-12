<template>
  <base-user-template>
    <div>
      <div class="container">
        <div class="left-div" style="width: 15%; float: left"></div>
        <div class="middle-div" style="width: 70%; float: left">
          <div v-if="Object.keys(this.users).length === 0">no request</div>

          <ui-grid class="demo-grid">
            <ui-grid-cell
              style="border: 1px solid"
              class="demo-cell"
              columns="3"
              v-for="(user, index) in users"
              :key="index"
            >
              <ui-card class="demo-card demo-card--photo">
                <ui-card-content class="demo-card__primary-action">
                  <ui-card-media
                    v-bind:style="{
                      'background-image': 'url(' + user.userProfilePhoto + ')',
                    }"
                    square
                    class="demo-card__media"
                  >
                    <ui-card-media-content
                      class="demo-card__media-content--with-title"
                    >
                      <div
                        :class="[$tt('subtitle2'), 'demo-card__media-title']"
                      >
                        {{ user.userUsername }}
                      </div>
                    </ui-card-media-content>
                  </ui-card-media>
                </ui-card-content>
                <ui-card-actions>
                  <ui-card-icons>
                    <ui-icon-button
                      :toggle="icon1"
                      @click="acceptUser(user.userId)"
                    ></ui-icon-button>
                  </ui-card-icons>
                </ui-card-actions>
              </ui-card>
            </ui-grid-cell>
          </ui-grid>
        </div>
        <div class="right-div" style="width: 15%; float: left"></div>
      </div>
    </div>
  </base-user-template>
</template>
        
      <script>
import BaseUserTemplate from "@/components/BaseUserTemplate.vue";
import { userConnectionApi } from "@/scripts/api/user_connection";
// import { userApi } from "@/scripts/api/user";
import { userProfilePhoto } from "@/scripts/api/user_profile_photo";

export default {
  data() {
    return {
      users: [],
      currentPage: 0,
      icon1: {
        on: "done_outline",
        off: "done",
      },
    };
  },
  async mounted() {
    await this.fetchUsers();
  },
  methods: {
    async acceptUser(userId) {
      userConnectionApi.sendConnectionRequest({ userId: userId });
    },

    async fetchUsers() {
      let t = await userConnectionApi.getRequests();

      this.users = t.userConnections;

      for (const userId of Object.keys(this.users)) {
        let r = await userProfilePhoto.getProfilePhoto({ userId: userId });

        this.users[userId]["userProfilePhoto"] = r["userProfilePhoto"];

        console.log("done");
      }
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
  