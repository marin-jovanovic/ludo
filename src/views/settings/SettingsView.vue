<template>
  <BaseUserTemplate>
    <div class="container-fluid">
      <div class="row">
        <h1>Settings</h1>
      </div>
      <div class="row">
        <BaseCheckbox
          :isSelectedInit="zoomUserLocation"
          @checkboxChange="zoomToggle"
          ref="zoom"
        ></BaseCheckbox>
        zoom on user location
      </div>
      <!-- <div class="row">style: <BaseCheckbox></BaseCheckbox></div> -->

      <BaseNotification ref="notifications"></BaseNotification>
    </div>
  </BaseUserTemplate>
</template>
  
  <script>
import BaseNotification from "@/components/BaseNotification.vue";
import { apiSettings } from "@/scripts/api/settings";
import BaseCheckbox from "../../components/BaseCheckbox.vue";
import BaseUserTemplate from "@/components/BaseUserTemplate.vue";
export default {
  data() {
    return {
      booleable: {
        zoomUserLocation: false,
      },
      zoomUserLocation: false,
    };
  },
  async mounted() {
    let r = await apiSettings.getSettings();
    if (r["auth"]["status"]) {
      let pl = r["payload"];

      console.log("pl", pl);

      this.zoomUserLocation = pl["zoomUserLocation"];
      this.$refs.zoom.isSelected = pl["zoomUserLocation"];
    }
  },
  methods: {
    updateStore(action, variable, value, message) {
      this.$store.dispatch(action, value);
      let curr = this.$store.getters[variable];

      this.$refs.notifications.showMessage(
        curr === value,
        `update: ${message} = ${value}`,
        `setting ${message} = ${value} error`
      );
    },

    async zoomToggle(isSelected) {
      console.log(isSelected);

      let r = await apiSettings.updateSettings({
        zoomUserLocation: isSelected,
      });
      if (r["auth"]["status"]) {
        let pl = r["payload"];

        console.log("pl", pl);

        this.zoomUserLocation = isSelected;
      }

      this.$refs.notifications.showMessage(
        r["payload"]["status"],
        `update: user zoom`,
        `error updating user zoom`
      );

      // let r = await apiSettings.getPortoflios();
      // if (r["auth"]["status"]) {
      //   let pl = r["payload"]["portfolios"];

      //   for (const [key, value] of Object.entries(pl)) {
      //     let hexColour = value["colour_hex"];

      //     let r = (await apiLocation.getAllLocationsInPortfolio(value.name))
      //       .payload.content;
      //     let marker = this.createMarker(hexColour);

      //     this.drawLocations(r, marker, key);
      //   }
      // }      // this.updateStore(
      //   "setZoomUserLocation",
      //   "zoomUserLocation",
      //   isSelected,
      //   "user zoom"
      // );
    },
  },
  components: { BaseCheckbox, BaseNotification, BaseUserTemplate },
};
</script>
  
  <style>
</style>