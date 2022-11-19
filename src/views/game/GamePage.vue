<template>
  <BaseUserTemplate>
    <!-- <hr /> -->
    <TheTest></TheTest>

    <TheActions></TheActions>

    <TheInfo ref="info"></TheInfo>

    <hr />
    <button @click="leaveGame">leave game</button>

    <button @click="test">test</button>

    <button @click="board">board scheme api</button>

    <div class="row">
      <div class="col">
        <TheGame></TheGame>
      </div>

      <div class="col">
        <div class="row">
          <div class="col">
            <TheDice ref="dice"></TheDice>
          </div>
          <div class="col">
            <button @click="rollDice">roll dice</button>
          </div>
        </div>
        <div class="row">
          <div class="col">
            <TheMessages></TheMessages>
          </div>
        </div>
      </div>
    </div>

    <hr />
  </BaseUserTemplate>
</template>


<script>
import TheInfo from "./TheInfo.vue";
import TheGame from "./TheGame.vue";
import TheDice from "./TheDice.vue";
import TheTest from "./../gameReplay/TheTest.vue";

import BaseUserTemplate from "@/components/BaseUserTemplate.vue";
import { apiLobby } from "@/scripts/api/lobby";
import { router } from "@/router/router";
import TheMessages from "./TheMessages.vue";
import { apiGame } from "@/scripts/api/game";
// import { wsListeners } from "@/scripts/ws_listener";
import { apiBoard } from "@/scripts/api/board";
import TheActions from "./TheActions.vue";

export default {
  data() {
    return {
      username: "",
      gameId: "",

      canRoll: false,
      rollResult: -1,

      instructionCurrentlyPerforming: -1,
      lastInstructionPerformed: -1,
    };
  },
  async mounted() {
    // let url = "ws://127.0.0.1:8000/game/";
    // new wsListeners.WebSocketListener(url, this.getUserActive);
    // console.log("ws init");

    this.username = sessionStorage.getItem("username");
    this.gameId = this.$route.params.id;

    let res = await apiGame.getGame(this.gameId);

    if (res["auth"]["status"] && res["payload"]["status"]) {
      let p = res["payload"]["payload"];

      console.table(p["log"]);

      for (const [key, value] of Object.entries(p["log"])) {
        console.log("instruction", key);

        if (value.action === "goes") {
          this.$refs.info.addToPlayingOrder(value.username);
        }

        // switch (value.action) {
        //   case "goes":
        //     break;

        //   default:
        //     break;
        // }

        if (value.performed) {
          await this.performed(value);
        } else {
          await this.notPefrormed(value, key);
          break;
        }

        // this.lastInstructionPerformed = key;
        // console.log("last perfromed", this.lastInstructionPerformed);
      }

      this.$refs.info.setHeader(p.header);
      this.$refs.info.setPlayers(p.players);
      // this.$refs.info.setHeader(p.header);
      // this.header = p.header;

      // this.players = p.players;
      // this.capacity = p.capacity;
    } else {
      console.log("err fetching data");
    }
  },
  methods: {
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

    // getUserActive(message) {
    //   console.log("ws msg received, todo");
    //   console.log(message);
    // },

    async notPerformedEnemyRoll() {
      console.log("enemy roll driver");
    },

    async notPerfrormedMyRoll(key, value) {
      this.canRoll = true;
      this.rollResult = value.diceResult;
      this.instructionCurrentlyPerforming = key;
    },

    async updateGame(token, action) {
      // post, do not know for what it is used
      let res = await apiGame.updateGame(
        this.gameId,
        this.username,
        token,
        action
      );

      if (!(res["auth"]["status"] && res["payload"]["status"])) {
        console.log("game leave err");
      }
    },

    async leaveGame() {
      let res = await apiLobby.leaveGame(this.gameId);

      if (res["auth"]["status"] && res["payload"]["status"]) {
        router.push("/");
      } else {
        console.log("[err] leave game");
      }
    },

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

    async actionPerformed() {
      // when user selects token to move || when user performs roll

      let res = await apiGame.actionPerformed(
        this.gameId,
        this.username,
        this.instructionCurrentlyPerforming
      );

      if (!(res["auth"]["status"] && res["payload"]["status"])) {
        console.log("game leave err");
      }
    },
  },
  components: {
    TheInfo,
    TheDice,
    BaseUserTemplate,
    TheMessages,
    TheGame,
    TheActions,
    TheTest,
  },
};
</script> 
