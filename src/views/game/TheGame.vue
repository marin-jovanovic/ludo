<template>
  <div>
    <br />
    user id
    <input v-model="userid" type="number" placeholder="1" />
    <br />
    token id
    <input v-model="tokenid" type="number" placeholder="1" />
    <br />
    jump count
    <input v-model="jump" type="number" placeholder="1" />
    <button @click="move">move</button>

    <div id="container" class="container">
      <canvas id="staticcanvas" width="600" height="600"></canvas>
      <canvas id="reactivecanvas" width="600" height="600">
        <!-- todo test -->
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

      userid: 0,
      tokenid: 0,
      jump: 5,
    };
  },
  async mounted() {
    this.initGame();
  },
  methods: {
    async move() {
      console.log(this.userid, this.tokenid, this.jump);

      this.movePosition({
        player: this.userid,
        token: this.tokenid,
        jumpCount: this.jump,
      });

      //  todo call backend
    },
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

/* .staticCanvas {
  border-style: dotted;
} */

.container > canvas {
  position: absolute;
  top: 0;
  left: 0;
}
</style>