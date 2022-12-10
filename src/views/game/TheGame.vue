<template>
  <div>
    <div id="container" class="container">
      <canvas
        ref="staticCanvas"
        id="staticcanvas"
        width="600"
        height="600"
      ></canvas>
      <canvas ref="reactiveCanvas" id="reactivecanvas" width="600" height="600">
        Your browser does not support the canvas element.
      </canvas>
    </div>
  </div>
</template>
    
<script>
import { ludo } from "@/views/game/ludo/scripts/index.js";
import { apiGameConfig } from "@/scripts/api/gameConfig";

export default {
  data() {
    return {
      game: undefined,
    };
  },
  async mounted() {
    this.initGame();
  },
  methods: {
    async initGame() {
      let config = ["startPool", "moves", "map", "players"];
      let gameId = this.$route.params.id;

      let configPayload = {};

      for (const i of config) {
        let res = await apiGameConfig.getResource(gameId, i);

        if (!(res["auth"]["status"] && res["payload"]["status"])) {
          console.log("fetch resource err");
          console.log("can not continue, abort");
        }

        configPayload[i] = res["payload"]["payload"];
      }

      this.game = new ludo.Game(
        document.querySelector("#staticcanvas"),
        document.querySelector("#reactivecanvas"),

        configPayload
      );
    },

    movePosition({ player, token, jumpCount }) {
      this.game.movePosition({
        player: player,
        token: token,
        jumpCount: jumpCount,
      });
    },
    restartToken({ player, token }) {
      this.game.restartToken({ player: player, token: token });
    },
  },
};
</script> 

<style>
.container {
  position: relative;
}

.container > canvas {
  position: absolute;
  top: 0;
  left: 0;
}
</style>