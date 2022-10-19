<template>
  <w-button bg-color="primary" dark @click="showOverlay = true">
    Show a blue overlay
  </w-button>

  <w-overlay v-model="showOverlay" bg-color="rgba(35, 71, 129, 0.4)">
    <!-- <w-button bg-color="primary" lg dark @click="showOverlay = false"> -->
    <!-- <w-icon class="mr2">wi-cross</w-icon>
      Hide overlay -->

    <TheMapOverlayMap></TheMapOverlayMap>
    <!-- <MapComponent ref="map"></MapComponent> -->
    <!-- </w-button> -->
  </w-overlay>
</template>

<script>
// import MapComponent from "./map/MapComponent.vue";
import TheMapOverlayMap from "./TheMapOverlayMap.vue";
export default {
  data() {
    return {
      showOverlay: false,
    };
  },
  components: { TheMapOverlayMap },
};
</script>

<style>
</style>