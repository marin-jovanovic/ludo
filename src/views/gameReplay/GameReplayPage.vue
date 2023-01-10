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

    <br />
    <hr />

    user join index:
    <input type="number" v-model="userJoinIndex" />

    token id:
    <input type="number" v-model="tokenId" />

    <button @click="move">move</button>

    <hr />

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
import TheDice from "@/components/TheDice.vue";

import BaseUserTemplate from "@/components/BaseUserTemplate.vue";

import { apiGame } from "@/scripts/api/game";
import { userMetaSS } from "@/scripts/session_storage";
import { apiBoard } from "@/scripts/api/board";
import { apiLevelLog } from "@/scripts/api/level_log";

export default {
  data() {
    return {
      userJoinIndex: 0,
      tokenId: 0,

      slider: 0,

      username: "",
      gameId: "",

      instructionId: -1,

      // changleLog : [],
      // isWaitingForAcceptance: false,

      p: undefined,
      // pp: undefined,
      diceTest: 1,
      // currInstruction: undefined,

      lastEntry: undefined,
    };
  },

  async mounted() {
    let flag = await this.$refs.game.initGame();
    // let flag = res["auth"]["status"] && res["payload"]["status"];

    if (!flag) {
      console.log("err");
      return;
    }

    this.username = userMetaSS.getCredentials()["username"];
    this.gameId = this.$route.params.id;

    // let res = await apiGame.getGame(this.gameId);

    this.currInstruction = 0;
  },
  methods: {
    async move() {
      console.log("moe", this.userJoinIndex, this.tokenId);

      let targetInstructionId = this.lastEntry.entryId;

      console.log("current instruction id", targetInstructionId);

      let t = await apiLevelLog.addToLog(
        this.gameId,
        this.tokenId,
        targetInstructionId
      );

      console.log(t);
    },

    async startReplay() {
      let res = await apiBoard.getLevel(this.gameId);

      // let res = await apiGame.getGame(this.gameId);

      console.log(res["players"]);

      let pp = res["players"];

      // username to join id

      const swapped = Object.entries(pp).map(([key, value]) => ({
        [value]: key,
      }));

      pp = Object.assign({}, ...swapped);

      // cons

      res = await apiLevelLog.getLevelLog(this.gameId);
      // console.log(res["log"]);

      let log = res["log"];

      for (const [instructionId, value] of Object.entries(log)) {
        console.log(instructionId, value);

        this.instructionId = instructionId;

        this.lastEntry = value;

        switch (value.action) {
          case "roll":
            console.log("roll");
            this.$refs.dice.rollDice(value.diceResult);
            break;

          case "goes":
            console.log("goes");
            console.log("[instruction] order ", value.userJoinIndex);
            break;

          case "move":
            console.log(
              instructionId,
              value.userJoinIndex,
              value.token,
              value.diceResult
            );

            this.$refs.game.movePosition(
              value.userJoinIndex,
              value.tokenId,
              value.diceResult
            );

            await this.sleep();

            break;

          case "choose":
            break;

          case "won":
            console.log("backend won", value.userJoinIndex);
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
      await apiGame.actionPerformed(this.gameId, this.username, action);
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
  