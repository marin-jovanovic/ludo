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
          </li>
          <li class="nav-item">
            <div>
              <ui-icon-button
                style="background-color: red"
                :toggle="icon1"
                @click="toggleMusic"
              ></ui-icon-button>
            </div>
            <!-- <router-link class="nav-link"> i.name </router-link> -->
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
        // index: { name: "Home", active: true },
        gameCreate: { name: "gameCreate", active: false },
        messages: { name: "Messages", active: false },
        findFriends: { name: "Find Friends", active: false },
        connectionRequest: { name: "Connection requests", active: false },
        statistics: { name: "Statistics", active: false },
      },
      icon1: {
        off: "play_arrow",
        on: "stop",
      },
      selectedSong: null,
      audioElement: null,
      songs: [
        { id: 1, title: "Song Corruption", url: "mp3/Corruption.mp3" },
        { id: 2, title: "Song 2", url: ".mp3" },
        { id: 3, title: "Song 3", url: ".mp3" },
      ],
    };
  },
  mounted() {
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
    toggleMusic() {
      if (!this.audioElement) {
        console.log("play");
        this.playMusic();
      } else {
        console.log("stop");
        this.stopMusic();
        this.audioElement = undefined;
      }
    },

    playMusic() {
      if (!this.audioElement) {
        this.audioElement = new Audio(this.selectedSong || this.songs[0].url);
      }
      this.audioElement.play();
    },
    pauseMusic() {
      if (this.audioElement) {
        this.audioElement.pause();
      }
    },
    stopMusic() {
      if (this.audioElement) {
        this.audioElement.pause();
        this.audioElement.currentTime = 0;
      }
    },

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