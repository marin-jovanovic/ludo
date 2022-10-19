/**
https://openlayers.org/en/latest/examples/popup.html
 */


<template>
  <div id="popup" class="ol-popup">
    <a href="#" id="popup-closer" class="ol-popup-closer"></a>
    <div v-if="visible" id="popup-content">
      <button @click="openDialog" class="btn btn-primary">
        Add this location
      </button>
      <div>
        {{ hdms }}
      </div>
    </div>
  </div>

  <TheDialogAddLocation ref="dialogBox"></TheDialogAddLocation>
</template>

<script>
import Overlay from "ol/Overlay";
import { toLonLat } from "ol/proj";
import { toStringHDMS } from "ol/coordinate";
import TheDialogAddLocation from "./TheDialogAddLocation.vue";

export default {
  data() {
    return {
      visible: true,
      overlay: undefined,
      closer: undefined,
      hdms: undefined,
    };
  },
  methods: {
    openDialog() {
      console.log("dialog opened");
      this.$refs.dialogBox.showDialog();
    },
    setText(hdms) {
      this.hdms = hdms;
    },
    setPosition(coordinate) {
      this.overlay.setPosition(coordinate);
    },
    getOverlay() {
      return this.overlay;
    },
    closePopup() {
      this.overlay.setPosition(undefined);
      this.closer.blur();
      return false;
    },
    clickEvent(evt) {
      const coordinate = evt.coordinate;
      const hdms = toStringHDMS(toLonLat(coordinate));
      this.setText(hdms);
      this.setPosition(coordinate);
      this.$store.dispatch("setClickedLocation", {
        longitude: toLonLat(coordinate)[0],
        latitude: toLonLat(coordinate)[1],
      });
    },
    closeWindow() {
      console.log("close window");
      this.$emit("closeAddingWindow");
    },
  },
  mounted() {
    /**
     * Elements that make up the popup.
     */
    const container = document.getElementById("popup");
    this.closer = document.getElementById("popup-closer");
    /**
     * Create an overlay to anchor the popup to the map.
     */
    this.overlay = new Overlay({
      element: container,
      autoPan: {
        animation: {
          duration: 250,
        },
      },
    });
    /**
     * Add a click handler to hide the popup.
     * @return {boolean} Don't follow the href.
     */
    this.closer.onclick = this.closeWindow;
  },
  components: { TheDialogAddLocation },
};
</script>

<style>
.ol-popup {
  position: absolute;
  background-color: white;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.2);
  padding: 15px;
  border-radius: 10px;
  border: 1px solid #cccccc;
  bottom: 12px;
  left: -50px;
  min-width: 280px;
}

.ol-popup:after,
.ol-popup:before {
  top: 100%;
  border: solid transparent;
  content: " ";
  height: 0;
  width: 0;
  position: absolute;
  pointer-events: none;
}

.ol-popup:after {
  border-top-color: white;
  border-width: 10px;
  left: 48px;
  margin-left: -10px;
}

.ol-popup:before {
  border-top-color: #cccccc;
  border-width: 11px;
  left: 48px;
  margin-left: -11px;
}

.ol-popup-closer {
  text-decoration: none;
  position: absolute;
  top: 2px;
  right: 8px;
}

.ol-popup-closer:after {
  content: "✖";
}
</style>