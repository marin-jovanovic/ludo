<template>
  <BaseUserTemplate>
    <button @click="test">test: generate random game</button>

    <input @change="sliderUpdate" type="range" min="0" max="5000" v-model="this.slider" />

    <hr />

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

import BaseUserTemplate from "@/components/BaseUserTemplate.vue";

import { apiGame } from "@/scripts/api/game";
import { apiBoard } from "@/scripts/api/board";

export default {
  data() {
    return {
      slider: 5000,

      username: "",
      gameId: "",

      canRoll: false,
      rollResult: -1,

      instructionCurrentlyPerforming: -1,
      lastInstructionPerformed: -1,
    };
  },

  async mounted() {
    this.username = sessionStorage.getItem("username");
    this.gameId = this.$route.params.id;

    let res = await apiGame.getGame(this.gameId);

    if (res["auth"]["status"] && res["payload"]["status"]) {
      let p = res["payload"]["payload"];

      let pp = p["players"]["payload"];
      const swapped = Object.entries(pp).map(([key, value]) => ({
        [value]: key,
      }));

      pp = Object.assign({}, ...swapped);

      for (const value of Object.values(p["log"])) {
        // console.log("instruction", key);

        switch (value.action) {
          case "roll":
            this.$refs.dice.rollDice(value.diceResult);
            break;

          case "goes":
            console.log("order ", value.username);
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
    } else {
      console.log("err fetching data");
    }
  },
  methods: {
    async sleep() {
      await new Promise((r) => setTimeout(r, this.slider));
    },

    sliderUpdate() {
      console.log("slider", this.slider);
    },

    async test() {
      // actionPerformed(game, player, instruction_id)

      let res = await apiGame.actionPerformed(
        this.gameId,
        this.username,
        "test"
        // this.instructionCurrentlyPerforming
      );

      if (!(res["auth"]["status"] && res["payload"]["status"])) {
        console.log("game leave err");
      }

      // res = await apiGame.getGame(this.gameId);

      // if (res["auth"]["status"] && res["payload"]["status"]) {
      //   let p = res["payload"]["payload"];

      //   console.table(p["log"]);

      //   for (const [key, value] of Object.entries(p["log"])) {
      //     console.log("instruction", key);

      //     if (value.action === "goes") {
      //       this.$refs.info.addToPlayingOrder(value.username);
      //     }

      //     if (value.performed) {
      //       await this.performed(value);
      //     } else {
      //       await this.notPefrormed(value, key);
      //       break;
      //     }
      //   }
      // } else {
      //   console.log("err fetching data");
      // }
    },

    async notPefrormed(value, key) {
      // for not performed instructions driver

      if (value.username == this.username) {
        console.log("your turn");

        switch (value.action) {
          case "roll":
            await this.notPerfrormedMyRoll(key, value);
            break;

          default:
            console.log("not handled action");
            break;
        }
      } else {
        console.log("waiting for player", value.username);

        switch (value.action) {
          case "roll":
            await this.notPerformedEnemyRoll();
            break;

          default:
            console.log("not handled action");
            break;
        }

        console.log("breaking");
        // break;
      }
    },
    async performed(value) {
      // for perfromred instructions driver

      console.log("this action is performed");

      if (value.username === this.username) {
        switch (value.action) {
          case "roll":
            break;
          default:
            console.log("not handled yet");
        }
      } else {
        console.log("someone else performed something");
      }
    },

    async board() {
      // for test
      let res = await apiBoard.getBoard("1", "startPool");

      console.log(res["payload"]["payload"]);

      if (!(res["auth"]["status"] && res["payload"]["status"])) {
        console.log("game leave err");
      }
    },

    async notPerformedEnemyRoll() {
      console.log("enemy roll driver");
    },

    async notPerfrormedMyRoll(key, value) {
      this.canRoll = true;
      this.rollResult = value.diceResult;
      this.instructionCurrentlyPerforming = key;
    },

    // async

    async rollDice() {
      // runner when user clicks to roll

      if (!this.canRoll) {
        console.log("can not roll");
        return;
      }

      this.canRoll = false;

      this.$refs.dice.rollDice(this.rollResult);

      await this.actionPerformed();
    },
  },
  components: { TheDice, BaseUserTemplate, TheGame },
};
</script> 
  