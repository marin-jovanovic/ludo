<template>
  <div @click="rollDice(5)" id="dice"></div>
  rolled : {{ this.value }}
</template>
  
  
<script>
import { dice } from "@/views/game/dice/index.js";

export default {
  data() {
    return {
      value: -1,
      diceElement: undefined,
    };
  },
  mounted() {
    this.diceElement = new dice.Dice({
      diceElement: document.querySelector("#dice"),
    });
  },
  methods: {
    rollDice(value) {
      // console.log("roll", value)

      this.value = value;

      this.diceElement.rollDice({ result: value });
    },
  },
};
</script> 
  
  <style>
@import "dice/index.css";

#d {
  border-style: dotted;
}
</style>