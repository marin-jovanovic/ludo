<template>
  <UserCoordinates
    @userCoordinates="drawUserLocation"
    :canSend="this.canSend"
    ref="userCoordinatesManager"
  >
  </UserCoordinates>
</template>



<script>
import { fromLonLat } from "ol/proj";
import Point from "ol/geom/Point";
import Feature from "ol/Feature";
import { Icon, Style } from "ol/style";
import VectorSource from "ol/source/Vector";
import { Vector as VectorLayer } from "ol/layer";

import userMarker from "/public/assets/markers/geolocation_marker.png";

import UserCoordinates from "@/components/UserCoordinates.vue";

export default {
  components: {
    UserCoordinates,
  },
  data() {
    return {
      addLocationEnabled: false,
      userLat: undefined,
      userLon: undefined,
      map: undefined,
      userLocationLayer: undefined,
      canSend: false,
      view: undefined,
      countriesLayer: undefined,
      portfolios: {},
      checkedNames: [],
    };
  },
  methods: {
    drawUserLocation(lat, lon) {
      console.log(lat, lon);

      this.userLat = this.$store.state.latitude;
      this.userLon = this.$store.state.longitude;

      const point = new Point(fromLonLat([lon, lat]));

      let feature = new Feature({
        geometry: point,
      });

      feature.setStyle(
        new Style({
          image: new Icon({
            src: userMarker,
            scale: 0.6,
          }),
        })
      );

      if (this.userLocationLayer) {
        this.map.removeLayer(this.userLocationLayer);
      }

      this.userLocationLayer = new VectorLayer({
        source: new VectorSource({
          features: [feature],
        }),
      });

      this.map.addLayer(this.userLocationLayer);

      let userZoom = this.$store.getters["zoomUserLocation"];

      console.log("user zoom", userZoom);
      if (userZoom) {
        this.view.centerOn(
          point.getCoordinates(),
          this.map.getSize(),
          [500, 500]
        );

        // zoom;
        this.view.fit(point, {
          padding: [170, 50, 30, 150],
          minResolution: 50,
        });

        // this.view.centerOn(
        //   point.getCoordinates(),
        //   this.map.getSize(),
        //   [500, 500]
        // );

        // // zoom;
        // this.view.fit(point, {
        //   padding: [170, 50, 30, 150],
        //   minResolution: 50,
        // });
      }
    },
  },

  async mounted() {
    this.map = this.$store.getters.map;

    this.activatePopup();

    // todo enable
    this.$refs.userCoordinatesManager.enableCoordinates();

    // await this.fetchLocations();
  },
};
</script>
