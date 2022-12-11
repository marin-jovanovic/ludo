<template>
  <div>
    <button @click="test">test: generate random game</button>

    <button @click="gostpnti">
      generate only start till player needs to interact
    </button>


  </div>
</template>
    
    
<script>
import { apiGame } from "@/scripts/api/game";

export default {
  data() {
    return {

    };
  },
  mounted() {},
  methods: {


    async performAction(action) {
      let res = await apiGame.actionPerformed(
        this.gameId,
        this.username,
        action
      );

      if (!(res["auth"]["status"] && res["payload"]["status"])) {
        console.log("game leave err");
      }
    },

    async gostpnti() {
      this.performAction("generatestart");
    },

    async test() {
      this.performAction("test");
    },
  },
};
</script> 
