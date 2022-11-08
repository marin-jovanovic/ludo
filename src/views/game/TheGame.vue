<template>
  <div>
    <canvas> </canvas>
  </div>
</template>
    
    
<script>
import { ludo } from "@/views/game/ludo/scripts/index.js";

export default {
  data() {
    return {
      // wait for one token to reach destination (stops moving) before other token can be moved on board
      backlog: [],
      useBacklog: false,
    };
  },
  mounted() {
    ludo.startup();

    if (this.useBacklog) {
      ludo.subscribe(this.notify);
    }
  },
  methods: {
    movePosition({ player, token, jumpCount }) {
      if (this.useBacklog) {
        if (this.backlog.length === 0) {
          ludo.movePosition({
            player: player,
            token: token,
            jumpCount: jumpCount,
          });
        }

        this.backlog.push([player, token, jumpCount]);
      } else {
        ludo.movePosition({
          player: player,
          token: token,
          jumpCount: jumpCount,
        });
      }
    },
    restartToken({ player, token }) {
      if (this.useBacklog) {
        if (this.backlog.length === 0) {
          ludo.restartToken({ player: player, token: token });
        }

        this.backlog.push([player, token]);
      } else {
        ludo.restartToken({ player: player, token: token });
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
