<template>
  <BaseUserTemplate>
    <TheTest></TheTest>

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
      <div class="col" style="border: 2px solid black">
        <TheGame ref="game" style="border: 2px solid black"></TheGame>
      </div>

      <div class="col">
        <div>turn:</div>
        <TheDice ref="dice"></TheDice>
      </div>
    </div>

    <hr />
  </BaseUserTemplate>
</template>
  
  
<script>
import TheGame from "./../game/TheGame.vue";
import TheDice from "./../game/TheDice.vue";
import TheTest from "./TheTest.vue";

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
  },
  components: { TheDice, BaseUserTemplate, TheGame, TheTest },
};
</script> 
  