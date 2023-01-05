<template>
  <div>
    <!-- <br />
    user id
    <input v-model="userid" type="number" placeholder="1" />
    <br />
    token id
    <input v-model="tokenid" type="number" placeholder="1" />
    <br />
    jump count
    <input v-model="jump" type="number" placeholder="1" />
    <button @click="move">move</button>

    <br />
    <button @click="testBlock">test block</button>

    <br />
    <button @click="fill">test fill</button>

    <br />
    <button @click="restr">test restricted</button>

    <br />
    <button @click="win">test win</button>

    <br />
    <button @click="bl">create block</button>

    <br />
    <button @click="guarded">test guarded part</button> -->

    <div
      style="border-style: solid; width: 700px; height: 700px"
      id="container"
      class="container"
    >
      <canvas id="staticcanvas"></canvas>
      <canvas id="reactivecanvas">
        <!-- <canvas id="staticcanvas" width="600" height="600"></canvas>
      <canvas id="reactivecanvas" width="600" height="600"> -->
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
    async win() {
      for (let playerId = 0; playerId < 4; playerId++) {
        for (let i = 0; i < 60; i++) {
          // move first
          this.movePosition({
            player: 0,
            token: playerId,
            jumpCount: 1,
          });
        }
      }
    },

    subscribe() {
      console.log("subs");
    },

    async guarded() {
      this.movePosition({
        player: 0,
        token: 0,
        jumpCount: 1,
      });
      this.movePosition({
        player: 0,
        token: 0,
        jumpCount: 55,
      });

      this.movePosition({
        player: 0,
        token: 1,
        jumpCount: 1,
      });
      this.movePosition({
        player: 0,
        token: 1,
        jumpCount: 53,
      });

      this.movePosition({
        player: 0,
        token: 2,
        jumpCount: 1,
      });
      this.movePosition({
        player: 0,
        token: 2,
        jumpCount: 51,
      });

      this.movePosition({
        player: 0,
        token: 1,
        jumpCount: 1,
      });
    },

    async bl() {
      this.movePosition({
        player: 0,
        token: 0,
        jumpCount: 1,
      });
      this.movePosition({
        player: 0,
        token: 1,
        jumpCount: 1,
      });
      this.movePosition({
        player: 0,
        token: 2,
        jumpCount: 1,
      });
      this.movePosition({
        player: 0,
        token: 3,
        jumpCount: 1,
      });
    },

    async restr() {
      // move first
      this.movePosition({
        player: 0,
        token: 0,
        jumpCount: 1,
      });
      this.movePosition({
        player: 0,
        token: 0,
        jumpCount: 55,
      });
      // move first
      this.movePosition({
        player: 0,
        token: 1,
        jumpCount: 1,
      });
      this.movePosition({
        player: 0,
        token: 1,
        jumpCount: 54,
      });
      this.movePosition({
        player: 0,
        token: 1,
        jumpCount: 1,
      });
      this.movePosition({
        player: 0,
        token: 1,
        jumpCount: 1,
      });
      this.movePosition({
        player: 0,
        token: 1,
        jumpCount: 1,
      });
    },

    async testBlock() {
      // move first
      this.movePosition({
        player: 0,
        token: 0,
        jumpCount: 1,
      });

      this.movePosition({
        player: 0,
        token: 0,
        jumpCount: 15,
      });

      // eat with second
      this.movePosition({
        player: 1,
        token: 0,
        jumpCount: 1,
      });

      this.movePosition({
        player: 1,
        token: 0,
        jumpCount: 2,
      });

      // form block
      this.movePosition({
        player: 1,
        token: 1,
        jumpCount: 1,
      });

      this.movePosition({
        player: 1,
        token: 1,
        jumpCount: 2,
      });

      // move first, try to eat
      this.movePosition({
        player: 0,
        token: 0,
        jumpCount: 1,
      });

      this.movePosition({
        player: 0,
        token: 0,
        jumpCount: 15,
      });

      // kill block
      this.movePosition({
        player: 1,
        token: 1,
        jumpCount: 1,
      });

      // move first, eat
      this.movePosition({
        player: 0,
        token: 0,
        jumpCount: 1,
      });

      this.movePosition({
        player: 0,
        token: 0,
        jumpCount: 15,
      });

      this.movePosition({
        player: 0,
        token: 0,
        jumpCount: 1,
      });
    },

    async fill() {
      for (let tokenId = 0; tokenId < 4; tokenId++) {
        for (let playerId = 0; playerId < 4; playerId++) {
          for (let i = 0; i < 70; i++) {
            this.movePosition({
              player: playerId,
              token: tokenId,
              jumpCount: 1,
            });
          }
        }
      }
    },

    async move() {
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

      // catch clicking on tokens

      this.game.ui.reactiveCanvas.subscribe({
        command: "tokenSelected",
        s: this.tokenSelected,
      });
    },

    tokenSelected({ username, tokenId }) {
      console.log("args");
      console.log(username, tokenId);
    },

    movePosition({ player, token, jumpCount }) {
      this.game.movePosition({
        playerId: player,
        tokenId: token,
        jumpCount: jumpCount,
      });
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