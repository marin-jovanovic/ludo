<template>
  <div id="map"></div>
</template>

<script>
import Map from "ol/Map";
import OSM from "ol/source/OSM";
import TileLayer from "ol/layer/Tile";
import View from "ol/View";
export default {
  data() {
    return {
      map: undefined,
    };
  },
  methods: {},
  mounted() {
    this.map = new Map({
      layers: [
        new TileLayer({
          source: new OSM(),
        }),
      ],
      target: "map",
      view: new View({
        center: [0, 0],
        zoom: 2,
      }),
    });

    this.$store.dispatch("setMap", this.map);
  },
};
</script>


<style>
#map {
  width: 90%;
  height: 90%;
  position: fixed;
  border: 1px solid #ccc;
}
</style>