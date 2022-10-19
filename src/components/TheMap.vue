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
  methods: {
    addLayer(layer) {
      this.map.addLayer(layer);
    },
  },
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

    // setTimeout(() => {
    //   this.map.updateSize();
    // });
  },
};
</script>


<style>
#map {
  width: 100%;
  height: 100%;
  position: absolute;
}
</style>