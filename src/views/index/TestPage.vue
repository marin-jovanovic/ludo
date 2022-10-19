<template>
  <TheMapFullSize ref="map"></TheMapFullSize>
  <TheAddLocationPopup ref="mappopup"></TheAddLocationPopup>

  <w-button
    class="ma1"
    @click="
      noOverlay = false;
      overlayColor = 'transparent';
      openDrawer = !openDrawer;
    "
    outline
  >
    Transparent overlay
  </w-button>
</template>
  
  <script>
import TheMapFullSize from "@/components/TheMap.vue";
import TheAddLocationPopup from "../../components/TheAddLocationPopup.vue";
import { apiPortfolio } from "@/scripts/api/portfolio";
import { apiLocation } from "@/scripts/api/location";
import { fromLonLat } from "ol/proj";
import Point from "ol/geom/Point";
import Feature from "ol/Feature";
import { Icon, Style } from "ol/style";
import VectorSource from "ol/source/Vector";
import { Vector as VectorLayer } from "ol/layer";

export default {
  components: {
    TheMapFullSize,

    TheAddLocationPopup,
  },
  data() {
    return {
      openDrawer: false,

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
  async mounted() {
    this.map = this.$refs.map.map;
    this.bindPopupToMap(this.map);

    // todo enable
    // this.$refs.userCoordinatesManager.enableCoordinates();

    await this.fetchLocations();
  },
  methods: {
    onChange() {
      for (const value of Object.values(this.portfolios)) {
        value["visible"] = false;
        this.map.removeLayer(value["vectorLayer"]);
      }

      this.checkedNames.forEach((i) => {
        this.portfolios[i]["visible"] = true;
      });

      for (const value of Object.values(this.portfolios)) {
        // value["visible"] = false;
        if (value["visible"]) {
          this.map.addLayer(value["vectorLayer"]);
        }
      }
    },
    drawLocations(featuresApi, marker, portfolioName) {
      let style = new Style({
        image: new Icon({
          src: "data:image/svg+xml;utf8," + marker,
          scale: 0.4,
        }),
      });

      let features = [];

      for (const value of Object.values(featuresApi)) {
        let f = new Feature({
          geometry: new Point(fromLonLat([value.lon, value.lat])),
        });

        f.setStyle(style);

        features.push(f);
      }

      const vectorLayer = new VectorLayer({
        source: new VectorSource({
          features: features,
        }),
      });
      this.portfolios[portfolioName] = {
        vectorLayer: vectorLayer,
      };
      this.map.addLayer(vectorLayer);
    },
    createMarker(hexColour) {
      return `
                  <svg viewBox="5 2 14 20" width="50" height="50" version="1.1" xmlns="http://www.w3.org/2000/svg">
                  <path d="M0 0h24v24H0z" fill="none"/>
                  <path fill="%23${hexColour}" d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z" />
                  </svg>
                  `;
    },
    async fetchLocations() {
      let r = await apiPortfolio.getPortoflios();
      if (r["auth"]["status"]) {
        let pl = r["payload"]["portfolios"];

        for (const [key, value] of Object.entries(pl)) {
          let hexColour = value["colour_hex"];

          let r = (await apiLocation.getAllLocationsInPortfolio(value.name))
            .payload.content;
          let marker = this.createMarker(hexColour);

          this.drawLocations(r, marker, key);
        }
      }
    },
    bindPopupToMap(map) {
      map.addOverlay(this.$refs.mappopup.getOverlay());
      map.on("singleclick", this.$refs.mappopup.clickEvent);
    },
    closePopup() {
      this.$refs.mappopup.closePopup();
    },
    openLeft() {
      console.log("left");
      this.openDrawer = !this.openDrawer;
    },
  },
};
</script>
  
  <style>
w-drawer {
  margin: 0;
  height: 100%;
  overflow: hidden;
  min-height: 75rem;
  /* padding-top: 4.5rem; */
  padding-top: 3.5rem;
}
</style>