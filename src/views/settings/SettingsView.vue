<template>
  <BaseUserTemplate>
    <div class="container-fluid">
      <div class="row">
        <h1>Settings</h1>
      </div>

      todo

      <BaseNotification ref="notifications"></BaseNotification>
    </div>
  </BaseUserTemplate>
</template>
  
<script>
import BaseNotification from "@/components/BaseNotification.vue";
import { apiSettings } from "@/scripts/api/settings";
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
    },
  },
  components: { BaseNotification, BaseUserTemplate },
};
</script>
  
<style>
</style>