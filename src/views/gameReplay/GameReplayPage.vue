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

    <div class="row">
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
      slider: 5000,

      username: "",
      gameId: "",
    };
  },

  async mounted() {
    this.username = sessionStorage.getItem("username");
    this.gameId = this.$route.params.id;

    // this.startReplay();
  },
  methods: {
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

      for (const value of Object.values(p["log"])) {
        switch (value.action) {
          case "roll":
            this.$refs.dice.rollDice(value.diceResult);
            break;

          case "goes":
            console.log("[instruction] order ", value.username);
            break;

          case "move":
            // console.log("move");

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

          case "eaten":
            // console.log("eat token");

            this.$refs.game.restartToken({
              player: pp[value.username],
              token: value.token,
            });

            await this.sleep();

            break;

          default:
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
  