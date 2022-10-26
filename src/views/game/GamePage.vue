<template>
  <BaseUserTemplate>
    <!-- <hr /> -->

    <h1>{{ this.header }}</h1>
    <br />
    <h2>order: {{ this.playingOrder }}</h2>
    <br />
    <button @click="leaveGame">leave game</button>
    <div>
      <div>players:</div>
      <div v-for="i in this.players" :key="i">p: {{ i }}</div>
    </div>
    <h1>now playing:</h1>

    <hr />

    <div class="row">
      <div class="col">
        <div class="row">
          <div class="col"></div>
          <div class="col">
            <TheDice ref="dice"></TheDice>
          </div>
          <div class="col">
            <button @click="rollDice">roll dice</button>
          </div>
        </div>
      </div>
      <div class="col"><TheMessages></TheMessages></div>
    </div>

    <TheGame></TheGame>

    <hr />
  </BaseUserTemplate>
</template>


<script>
import TheGame from "./TheGame.vue";
import TheDice from "./TheDice.vue";
import BaseUserTemplate from "@/components/BaseUserTemplate.vue";
import { apiLobby } from "@/scripts/api/lobby";
import { router } from "@/router/router";
import TheMessages from "./TheMessages.vue";
import { apiGame } from "@/scripts/api/game";
// import { wsListeners } from "@/scripts/ws_listener";

export default {
  data() {
    return {
      canRoll: false,
      rollResult: -1,

      username: "",
      header: "",

      gameId: "",

      players: {},
      capacity: -1,

      instructionCurrentlyPerforming: -1,

      lastInstructionPerformed: -1,

      playingOrder: [],
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

        switch (value.action) {
          case "goes":
            this.playingOrder.push(value.username);
            this.instructionCurrentlyPerforming = key;
            this.lastInstructionPerformed = key;

            await this.actionPerformed();

            break;

          default:
            break;
        }

        if (!value.performed) {
          if (value.username == this.username) {
            console.log("your turn");

            switch (value.action) {
              case "roll":
                await this.rollDriver(key, value);
                break;

              default:
                console.log("not handled action");
                break;
            }
          } else {
            console.log("waiting for player", value.username);

            switch (value.action) {
              case "roll":
                await this.enemyRollDriver();
                break;

              default:
                console.log("not handled action");
                break;
            }

            console.log("breaking");
            break;
          }
        } else {
          console.log("this action is performed");

          if (value.username === this.username) {
            switch (value.action) {
              case "roll":
                this.$refs.dice.rollDice(value.diceResult);
                break;
              default:
                console.log("not handled yet");
            }
          } else {
            console.log("someone else performed something");
          }
        }

        this.lastInstructionPerformed = key;
        console.log("last perfromed", this.lastInstructionPerformed);
      }

      this.header = p.header;

      this.players = p.players;
      this.capacity = p.capacity;
    } else {
      console.log("err fetching data");
    }
  },
  methods: {
    getUserActive(message) {
      console.log("ws msg received, todo");
      console.log(message);
    },

    async enemyRollDriver() {
      console.log("enemy roll driver");
    },

    async rollDriver(key, value) {
      console.log("roll", value.diceResult);
      this.canRoll = true;
      this.rollResult = value.diceResult;
      this.instructionCurrentlyPerforming = key;
    },

    async updateGame(token, action) {
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
      if (!this.canRoll) {
        console.log("can not roll");
        return;
      }

      this.canRoll = false;

      this.$refs.dice.rollDice(this.rollResult);

      await this.actionPerformed();
    },

    async actionPerformed() {
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
  components: { TheDice, BaseUserTemplate, TheMessages, TheGame },
};
</script> 
