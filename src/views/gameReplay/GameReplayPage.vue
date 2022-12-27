<template>
  <BaseUserTemplate>
    <div>
      <button @click="test">test: generate random game</button>

      <button @click="gostpnti">
        generate only start till player needs to interact
      </button>
    </div>

    <input
      @change="sliderUpdate"
      type="range"
      min="0"
      max="5000"
      v-model="this.slider"
    />

    <hr />

    <button @click="startReplay">start replay</button>

    <button @click="replayStep">next instruction</button>

    <div class="row">
      <div>instruction id {{ this.instructionId }}</div>
      <div class="col">
        <TheGame ref="game"></TheGame>
      </div>

      <div class="col">
        <div>turn:</div>
        <TheDice ref="dice"></TheDice>
      </div>
    </div>
  </BaseUserTemplate>
</template>
  
  
<script>
import TheGame from "./../game/TheGame.vue";
import TheDice from "./../game/TheDice.vue";

import BaseUserTemplate from "@/components/BaseUserTemplate.vue";

import { apiGame } from "@/scripts/api/game";

export default {
  data() {
    return {
      slider: 0,

      username: "",
      gameId: "",

      instructionId: -1,

      // changleLog : [],
      // isWaitingForAcceptance: false,

      p: undefined,
      pp: undefined,
      // currInstruction: undefined,
    };
  },

  async mounted() {
    this.username = sessionStorage.getItem("username");
    this.gameId = this.$route.params.id;

    // this.$refs.game.subscribe({
    //   command: "animateTokens",
    //   s: this.ui.reactiveCanvas.animate
    // });

    // this.bl.currentLevel.subscribe({
    //         command: "animateTokens",
    //         s: this.ui.reactiveCanvas.animate
    //     });

    // this.startReplay();

    let res = await apiGame.getGame(this.gameId);

    if (!(res["auth"]["status"] && res["payload"]["status"])) {
      console.log("err fetching data");
      return;
    }

    this.p = res["payload"]["payload"];

    let pp = this.p["players"]["payload"];
    const swapped = Object.entries(pp).map(([key, value]) => ({
      [value]: key,
    }));

    this.pp = Object.assign({}, ...swapped);

    console.log(this.p);

    this.currInstruction = 0;
  },
  methods: {
    // updated() {
    //     /**
    //      * callback for updating ui
    //      */

    //     // todo check for race condition

    //     if (this.changleLog.length === 0) {

    //         this.isWaitingForAcceptance = false;

    //     } else {

    //         let oldest = this.changleLog[0];

    //         let oldestMove = oldest.move;
    //         let oldestToken = oldest.token;

    //         oldestToken.notify({
    //             command: "newDestination",
    //             diff: oldestMove
    //         })

    //         this.changleLog.shift();

    //     }

    // },

    async replayStep() {
      let value = this.p["log"][this.instructionId];
      this.instructionId++;

      // for (const [instructionId, value] of Object.entries(this.p["log"])) {
      // if (instructionId > 30) {
      //   return;
      // }

      console.log(this.instructionId);
      switch (value.action) {
        case "roll":
          this.$refs.dice.rollDice(value.diceResult);
          break;

        case "goes":
          console.log("[instruction] order ", value.username);
          break;

        case "move":
          this.$refs.game.movePosition({
            player: this.pp[value.username],
            token: value.token,
            jumpCount: value.diceResult,
          });

          await this.sleep();

          break;

        case "won":
          console.log("won", value.username);
          break;

        default:
          console.log("unknown command", value.action);
          break;
      }
      // }
    },

    async startReplay() {
      let res = await apiGame.getGame(this.gameId);

      if (!(res["auth"]["status"] && res["payload"]["status"])) {
        console.log("err fetching data");
        return;
      }

      let p = res["payload"]["payload"];

      let pp = p["players"]["payload"];
      const swapped = Object.entries(pp).map(([key, value]) => ({
        [value]: key,
      }));

      pp = Object.assign({}, ...swapped);

      console.log(p);

      for (const [instructionId, value] of Object.entries(p["log"])) {
        // if (instructionId > 307) {
        //   return;
        // }

        console.log(instructionId);
        this.instructionId = instructionId;
        switch (value.action) {
          case "roll":
            this.$refs.dice.rollDice(value.diceResult);
            break;

          case "goes":
            console.log("[instruction] order ", value.username);
            break;

          case "move":
            this.$refs.game.movePosition({
              player: pp[value.username],
              token: value.token,
              jumpCount: value.diceResult,
            });

            await this.sleep();

            break;

          case "won":
            console.log("won", value.username);
            break;

          default:
            console.log("unknown command", value.action);
            break;
        }
      }
    },
    async sleep() {
      await new Promise((r) => setTimeout(r, this.slider));
    },

    sliderUpdate() {
      console.log("slider", this.slider);
    },

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
  components: { TheDice, BaseUserTemplate, TheGame },
};
</script> 
  