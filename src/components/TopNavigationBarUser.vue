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
        <a
          class="nav-link dropdown-toggle ms-2"
          href="#"
          role="button"
          data-bs-toggle="dropdown"
          aria-expanded="false"
        >
          {{ username }}
          <!-- {{ this.$store.getters.username }} -->
          <i class="bi bi-person-fill"></i>
        </a>
        <ul class="dropdown-menu dropdown-menu-end">
          <li>
            <router-link class="dropdown-item" to="/settings"
              >Settings</router-link
            >
          </li>
          <li>
            <router-link class="dropdown-item" to="/logout">Logout</router-link>
          </li>
        </ul>
      </li>
    </ul>
  </div>
</template>

<script>
import { apiSettings } from "@/scripts/api/settings";

export default {
  data() {
    return { username: undefined };
  },
  async mounted() {
    // console.log("get username");

    let r = await apiSettings.getSettings();
    if (r["auth"]["status"]) {
      let pl = r["payload"];

      // console.log("pl", pl);

      this.username = pl["username"];
    }
  },
};
</script>

<style>
</style>