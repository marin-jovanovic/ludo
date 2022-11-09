<template>
  <div>
    <canvas> </canvas>
  </div>
</template>
    
    
<script>
import { ludo } from "@/views/game/ludo/scripts/index.js";
import { apiGameConfig } from "@/scripts/api/gameConfig";

export default {
  data() {
    return {
      // wait for one token to reach destination (stops moving) before other token can be moved on board
      backlog: [],
      useBacklog: false,
    };
  },
  async mounted() {

    this.initGame();

    if (this.useBacklog) {
      ludo.subscribe(this.notify);
    }
  },
  methods: {
    async initGame() {
      let config = ['startPool', 'moves', 'map', 'players'];
      let gameId = this.$route.params.id;

      let configPayload = {};

      for (const i of config) {

        let res = await apiGameConfig.getResource(
          gameId,
          i
        );

        if (!(res["auth"]["status"] && res["payload"]["status"])) {
          console.log("fetch resource err");
          console.log('can not continue, abort')
        }

        configPayload[i] = res['payload']['payload'];

      }

      ludo.getGame().setConfig(configPayload);

    },

    movePosition({ player, token, jumpCount }) {
      if (this.useBacklog) {
        if (this.backlog.length === 0) {
          ludo.game.movePosition({
            player: player,
            token: token,
            jumpCount: jumpCount,
          });
        }

        this.backlog.push([player, token, jumpCount]);
      } else {
        ludo.getGame().movePosition({
          player: player,
          token: token,
          jumpCount: jumpCount,
        });
      }
    },
    restartToken({ player, token }) {
      if (this.useBacklog) {
        if (this.backlog.length === 0) {
          ludo.getGame().restartToken({ player: player, token: token });
        }

        this.backlog.push([player, token]);
      } else {
        ludo.getGame().restartToken({ player: player, token: token });
      }
    },

    notify() {
      this.backlog.shift();

      if (this.backlog.length === 0) {
        return;
      }

      let first = this.backlog[0];

      if (first.length === 2) {
        ludo.restartToken({ player: first[0], token: first[1] });
      } else {
        ludo.movePosition({
          player: first[0],
          token: first[1],
          jumpCount: first[2],
        });
      }
    },
  },
};
</script> 
