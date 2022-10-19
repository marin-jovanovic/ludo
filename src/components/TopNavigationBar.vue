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

            <!-- <router-link
              v-if="!i.active"
              @click="clicked(j)"
              class="nav-link"
              :to="{ name: j }"
              >{{ i.name }}</router-link
            >

            <router-link v-else class="nav-link active" :to="{ name: j }">{{
              i.name
            }}</router-link> -->
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
        portfolio: { name: "Portfolio", active: false },
        test: { name: "test_test", active: true },
        history: { name: "todo_history", active: false },
      },
      links: [
        { pathName: "index", name: "Home", active: true },
        { pathName: "portfolio", name: "Portfolio", active: false },
        { pathName: "login", name: "test_login", active: false },
        { pathName: "test", name: "test_test", active: false },
        { pathName: "history", name: "todo_history", active: false },
      ],
    };
  },
  methods: {
    clicked(i) {
      console.log("clicked", i.pathName, i.name, i.active);
      for (const [key, value] of Object.entries(this.linksD)) {
        console.log(key, value);
        value.active = false;
        // value.name = "brrrrrrrr";
      }

      this.linksD[i].active = true;
      // console.log(i.active);
      // this.links.forEach((j) => {
      //   j.active = false;
      // });
      // i.name = "fffffff";
      // i.active = true;
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
