<template>
  <div></div>
  <!-- your coordinates -->
  <!-- <input type="text" v-model="lat" :name="lat" class="form-control" /> -->
  <!-- <input type="text" v-model="lon" :name="lon" class="form-control" /> -->
  <!-- <button @click="$emit('userCoordinates', this.lat, this.lon)">click me</button> -->
  <!-- <button @click="emitCoordinates()">zoom on my location</button> -->
</template>

<script>
import { apiExternal } from "@/scripts/api/external";

export default {
  props: { canSend: Boolean },
  emits: ["userCoordinates"],
  data() {
    return {
      lat: 0,
      lon: 0,
      canEmit: false,
    };
  },
  methods: {
    enableCoordinates() {
      this.canEmit = true;
    },
    emitCoordinates() {
      if (this.canEmit) {
        this.$emit("userCoordinates", this.lat, this.lon);
      }
    },
    displayUserCoordinatesWillingly() {
      navigator.geolocation.getCurrentPosition(
        this.showPosition,
        this.showError,
        { timeout: 5000 }
      );
    },
    async displayUserCoordinatesUnwillingly() {
      let r = await apiExternal.getCoordinates();
      this.showPosition({
        coords: r,
      });
    },
    showPosition(position) {
      this.$store.dispatch("setUserCoordinates", {
        latitude: position.coords.latitude,
        longitude: position.coords.longitude,
      });

      this.lat = position.coords.latitude;
      this.lon = position.coords.longitude;
      this.emitCoordinates();
    },
    showError() {
      this.displayUserCoordinatesUnwillingly();
    },
  },
  mounted() {
    this.emitCoordinates();

    if (navigator.geolocation) {
      this.displayUserCoordinatesWillingly();
    } else {
      alert("Geolocation is not supported by this browser");
      this.displayUserCoordinatesUnwillingly();
    }
  },
};
</script>