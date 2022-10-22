<template>
  <div class="dice"></div>
</template>
  
  
<script>
import { dice } from "@/views/game/dice/index.js";

export default {
  data() {
    return {};
  },
  mounted() {
    dice.startup();
  },
  methods: {
    rollDice() {
      dice.rollDice(5);
    },
  },
};
</script> 
  
  <style>
@import "dice/index.css";
</style>