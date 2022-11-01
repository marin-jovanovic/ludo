<template>
  <div>
    <button id="ulul">ul ul</button>
    <button id="ulur">ul ur</button>
    <button id="uldl">ul dl</button>
    <button id="uldr">ul dr</button>
    <br />
    <button id="rulul">ret ul ul</button>
    <button id="rulur">ret ul ur</button>
    <button id="ruldl">ret ul dl</button>
    <button id="ruldr">ret ul dr</button>

    <hr />

    <canvas> </canvas>
  </div>
</template>
    
    
  <script>
import { ludo } from "@/views/game/ludo/scripts/index.js";

export default {
  data() {
    return {};
  },
  mounted() {
    ludo.startup();
  },
  methods: {
    movePosition({ player, token, jumpCount }) {
      ludo.movePosition({ player: player, token: token, jumpCount: jumpCount });
      // ludo.movePosition({player, token, jumpCount}
    },
  },
};
</script> 
    
    <!-- <style>
@import "ludo/index.css";
</style> -->

  
  
