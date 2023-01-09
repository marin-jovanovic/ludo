<template>
  <router-view> </router-view>
</template>

<style>
@import "https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css";
@import "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.4.1/font/bootstrap-icons.css";
@import "https://cdn.jsdelivr.net/npm/@mdi/font@5.8.55/css/materialdesignicons.min.css";
@import "https://use.fontawesome.com/releases/v5.2.0/css/all.css";
@import "balm-ui/dist/balm-ui.css";

body {
  background-image: url("/public/jpg/pexels-johannes-plenio-1103970.jpg");
  background-repeat: no-repeat;
  background-attachment: fixed;
  background-size: 100% 100%;
}
</style>

<script>
import { router } from "./router/router";
import { INACTIVE_THRESHOLD, TIME_RESOLUTION } from "./scripts/constants";
import { apiAuth } from "./scripts/api/auth";
import { userMetaSS } from "./scripts/session_storage";

export default {
  data() {
    return {
      isInactive: false,
      userActivityThrottlerTimeout: null,
      userActivityTimeout: null,
    };
  },
  mounted() {
    this.importScript(
      "http://ajax.googleapis.com/ajax/libs/jquery/1.7/jquery.min.js"
    );

    this.importScript("https://cdn.jsdelivr.net/npm/sweetalert2@8");

    this.importScript(
      "https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js"
    );
    this.importScript(
      "https://cdn.jsdelivr.net/npm/chart.js@3.0.2/dist/chart.min.js"
    );
    this.importScript("https://code.jquery.com/jquery-3.5.1.slim.min.js");
  },
  methods: {
    importScript(path) {
      let scriptElement = document.createElement("script");
      scriptElement.setAttribute("src", path);
      document.head.appendChild(scriptElement);
    },
    activateActivityTracker() {
      window.addEventListener("mousemove", this.userActivityThrottler);
      window.addEventListener("scroll", this.userActivityThrottler);
      window.addEventListener("keydown", this.userActivityThrottler);
      window.addEventListener("resize", this.userActivityThrottler);
    },
    deactivateActivityTracker() {
      window.removeEventListener("mousemove", this.userActivityThrottler);
      window.removeEventListener("scroll", this.userActivityThrottler);
      window.removeEventListener("keydown", this.userActivityThrottler);
      window.removeEventListener("resize", this.userActivityThrottler);
    },
    resetUserActivityTimeout() {
      clearTimeout(this.userActivityTimeout);
      this.userActivityTimeout = setTimeout(() => {
        this.userActivityThrottler();
        this.inactiveUserAction();
      }, INACTIVE_THRESHOLD);
    },
    userActivityThrottler() {
      if (this.isInactive) {
        this.isInactive = false;
      }
      if (!this.userActivityThrottlerTimeout) {
        this.userActivityThrottlerTimeout = setTimeout(() => {
          this.resetUserActivityTimeout();
          clearTimeout(this.userActivityThrottlerTimeout);
          this.userActivityThrottlerTimeout = null;
        }, TIME_RESOLUTION);
      }
    },
    inactiveUserAction() {
      if (window.location.href.endsWith("login")) {
        return;
      }
      apiAuth.logout();
      router.push("login");
      this.isInactive = true;
    },
  },
  beforeMount() {
    // this.activateActivityTracker();
  },
  beforeUnmount() {
    // this.deactivateActivityTracker();
    // clearTimeout(this.userActivityTimeout);
    // clearTimeout(this.userActivityThrottlerTimeout);

    userMetaSS.logout();
  },
};
</script>