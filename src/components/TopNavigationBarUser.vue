<template>
  <button
    class="navbar-toggler"
    type="button"
    data-bs-toggle="collapse"
    data-bs-target="#topNavBar"
    aria-controls="topNavBar"
    aria-expanded="false"
    aria-label="Toggle navigation"
  >
    <span class="navbar-toggler-icon"></span>
  </button>

  <div class="collapse navbar-collapse" id="topNavBar">
    <form class="d-flex ms-auto my-3 my-lg-0"></form>
    <ul class="navbar-nav">
      <li class="nav-item dropdown">
        <!-- {{ this.$store.getters.username }} -->
        <!-- <i class="bi bi-person-fill"></i> -->
        {{ username }}

        <!-- <a
          class="nav-link dropdown-toggle ms-2"
          href="#"
          role="button"
          data-bs-toggle="dropdown"
          aria-expanded="false"
        > -->

        <a href="#" data-bs-toggle="dropdown">
          <top-navigation-bar-profile-picture></top-navigation-bar-profile-picture>
        </a>
        <ul class="dropdown-menu dropdown-menu-end">
          <li v-for="i in this.links" :key="i">
            <router-link class="dropdown-item" :to="i.to">{{
              i.name
            }}</router-link>
          </li>
        </ul>
      </li>
    </ul>
  </div>
</template>
  
<script>
import TopNavigationBarProfilePicture from "./TopNavigationBarProfilePicture.vue";

import { apiSettings } from "@/scripts/api/settings";
export default {
  data() {
    return {
      username: undefined,
      profilePhoto: undefined,

      links: [
        { to: "/settings", name: "Settings" },
        { to: "/logout", name: "Logout" },
        { to: "/messages", name: "Messages" },
      ],
    };
  },
  async mounted() {
    let r = await apiSettings.getSettings();

    this.username = r["username"];
  },
  components: {
    TopNavigationBarProfilePicture,
  },
};
</script>
  
<style>
</style>