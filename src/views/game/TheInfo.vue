<template>
  <div id="info">
    <h1>{{ this.header }}</h1>
    <br />
    <h2>order: {{ this.playingOrder }}</h2>
    <br />
    <div>
      <div>players:</div>
      <div v-for="i in this.players" :key="i">p: {{ i }}</div>
    </div>
    <h1>now playing:</h1>
  </div>
</template>
      
      
    <script>
export default {
  data() {
    return {
      header: "",
      playingOrder: [],
      players: {},
    };
  },
  mounted() {},
  methods: {
    setHeader(header) {
      this.header = header;
    },
    setPlayingOrder(playingOrder) {
      this.playingOrder = playingOrder;
    },
    setPlayers(players) {
      this.players = players;
    },
    addToPlayingOrder(username) {
      this.playingOrder.push(username);
    },
  },
};
</script> 

<style>
#info {
  background-color: lightblue;
}
</style>