<template>
  <BaseUserTemplate>
    <!-- <hr /> -->
    <h1>{{ this.header }}</h1>
    <br />

    <button @click="leaveGame">leave game</button>

    <div>
      <div>players:</div>
      <div v-for="i in this.players" :key="i">p: {{ i }}</div>
    </div>

    <h1>now playing:</h1>

    <div class="row">
      <div class="col"></div>
      <div class="col">
        <TheDice ref="dice"></TheDice>
      </div>
      <div class="col">
        <button @click="rollDice">roll dice</button>
      </div>
    </div>

    <div>
      <button>move 1</button>
      <button>move 2</button>
      <button>move 3</button>
      <button>move 4</button>
    </div>

    <hr />

    <div>
      token

      <input type="text" v-model="cToken" />
      <br />

      action
      <input type="text" v-model="cAction" />
      <br />

      <button @click="updateGame">submit</button>
    </div>
    <hr />
    <TheMessages></TheMessages>

    <div class="row"></div>
  </BaseUserTemplate>
</template>


<script>
import TheDice from "./TheDice.vue";
import BaseUserTemplate from "@/components/BaseUserTemplate.vue";
import { apiLobby } from "@/scripts/api/lobby";
import { router } from "@/router/router";
import TheMessages from "./TheMessages.vue";
import { apiGame } from "@/scripts/api/game";

export default {
  data() {
    return {
      canRoll: true,
      username: "",
      header: "",

      // todo rewrite url with this
      gameId: "",

      players: {},
      capacity: -1,

      cToken: "",
      cAction: "",
    };
  },
  async mounted() {
    this.username = sessionStorage.getItem("username");
    this.gameId = sessionStorage.getItem("gameId");

    let res = await apiGame.getGame(this.gameId);
    if (res["auth"]["status"]) {
      let p = res["payload"]["payload"];

      console.table(p);

      this.header = p.header;

      if (p.turn === this.username) {
        this.canRoll = true;
      } else {
        this.canRoll = false;
      }

      this.players = p.players;
      this.capacity = p.capacity;
    } else {
      console.log("err fetching data");
    }

    // for (const [key, value] of Object.entries(this.players)) {
    //   console.log(key, value);
    //   console.log("roll player", value);
    // }
  },
  methods: {
    async updateGame() {
      let res = await apiGame.updateGame(
        this.gameId,
        this.username,
        this.cToken,
        this.cAction
      );

      if (res["auth"]["status"]) {
        if (!res["payload"]["status"]) {
          console.log("game leave err");
        }
      } else {
        console.log("err update");
      }
    },

    async leaveGame() {
      let res = await apiLobby.leaveGame(this.gameId);
      if (res["auth"]["status"]) {
        if (res["payload"]["status"]) {
          router.push("/");
        } else {
          console.log("game leave err");
        }
      }
    },

    rollDice() {
      if (!this.canRoll) {
        console.log("can not roll");
        return;
      }

      this.$refs.dice.rollDice(5);
    },
  },
  components: { TheDice, BaseUserTemplate, TheMessages },
};
</script> 

<style>
.col {
  border: 1mm solid black;
}
</style>