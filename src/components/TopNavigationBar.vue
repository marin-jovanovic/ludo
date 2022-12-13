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
          <li v-for="(i, j) in linksD" :key="i" class="nav-item">
            <router-link class="nav-link" :to="{ name: j }">{{
              i.name
            }}</router-link>
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
      linksD: {
        index: { name: "Home", active: true },
        gameCreate: { name: "gameCreate", active: false },
        // gameReplay: { name: "gameReplay", active: false },
      },
      links: [{ pathName: "index", name: "Home", active: true }],
    };
  },
  methods: {
    clicked(i) {
      console.log("clicked", i.pathName, i.name, i.active);
      for (const [key, value] of Object.entries(this.linksD)) {
        console.log(key, value);
        value.active = false;
      }
      this.linksD[i].active = true;
    },
    setActive(p) {
      console.log("set", p);
    },
  },
  components: { TopNavigationBarName, TopNavigationBarUser },
};
</script>
  
<style>
</style>