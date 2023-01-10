<template>
  <nav class="navbar navbar-expand-md navbar-dark fixed-top bg-dark">
    <div class="container-fluid">
      <TopNavigationBarName></TopNavigationBarName>
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarCollapse"
        aria-controls="navbarCollapse"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarCollapse">
        <ul class="navbar-nav me-auto mb-2 mb-md-0">
          <li v-for="(i, j) in links" :key="i" class="nav-item">
            <div v-if="i.active">
              <router-link class="nav-link active" :to="{ name: j }">{{
                i.name
              }}</router-link>
            </div>

            <div v-else>
              <router-link
                @click="clicked(i)"
                class="nav-link"
                :to="{ name: j }"
                >{{ i.name }}</router-link
              >
            </div>

            <!-- <router-link
              @click="clicked(i)"
              class="nav-link"
              :to="{ name: j }"
              >{{ i.name }}</router-link
            > -->
          </li>
        </ul>
      </div>

      <TopNavigationBarUser></TopNavigationBarUser>
    </div>
  </nav>
</template>
  
<script>
import TopNavigationBarName from "./TopNavigationBarName.vue";
import TopNavigationBarUser from "./TopNavigationBarUser.vue";
export default {
  data() {
    return {
      links: {
        index: { name: "Home", active: true },
        gameCreate: { name: "gameCreate", active: false },
        messages: { name: "Messages", active: false },
        // setting: { name: "Messages", active: false },

        // gameReplay: { name: "gameReplay", active: false },
      },
    };
  },
  mounted() {
    // console.log(this.$router.currentRoute);

    // console.log(this.$router);
    // console.log(this.$route);

    let currentPath = this.$route.name;

    for (const value of Object.values(this.links)) {
      value.active = false;
    }

    if (!(currentPath in this.links)) {
      return;
    }

    this.links[currentPath].active = true;
  },

  methods: {
    clicked(i) {
      for (const value of Object.values(this.links)) {
        value.active = false;
      }

      i.active = true;

      // todo localstorage
      // err ocurs if refresh site on e.g. /messages because link is not acitve
    },
  },
  components: { TopNavigationBarName, TopNavigationBarUser },
};
</script>
  
<style>
</style>