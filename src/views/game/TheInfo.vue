<template>
  <div id="info">
    <h3>order</h3>
    <div v-for="(i, index) in this.playingOrder" :key="index">
      {{ index }} -> {{ i }}
    </div>

    <br />

    <h1>now playing:</h1>
  </div>
</template>
      

      
<script>
import { levelSessionStorage } from "@/scripts/session_storage";
import { setPlayingOrder } from "@/scripts/set_playing_order";

export default {
  data() {
    return {
      playingOrder: [],
      players: {},
    };
  },
  async mounted() {
    let levelId = levelSessionStorage.getLevelMeta()["levelId"];

    await setPlayingOrder({ levelId: levelId });

    this.playingOrder = levelSessionStorage.getLevelMeta()["order"];
  },
  methods: {},
};
</script> 

<style>
#info {
  background-color: lightblue;
}
</style>