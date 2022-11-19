<template>
  <div class="dice"></div>
  rolled : {{ this.value }}
</template>
  
  
<script>
import { dice } from "@/views/game/dice/index.js";

export default {
  data() {
    return {
      value: -1,
    };
  },
  mounted() {
    dice.startup();
  },
  methods: {
    rollDice(value) {
      this.value = value;
      dice.rollDice(value);
    },
  },
};
</script> 
  
  <style>
@import "dice/index.css";
</style>