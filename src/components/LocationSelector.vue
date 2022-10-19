<template>
  <div>
    <div>enter location</div>

    <InputAutocomplete
      @input="userTypedLocation"
      ref="inputautocompletefield"
      :initItems="[]"
    >
    </InputAutocomplete>

    <button @click="buttonClicked">search</button>
  </div>
</template>

<script>
import InputAutocomplete from "./../form/InputAutocomplete.vue";
import { jsonManager } from "../scripts/json_manager";

export default {
  components: {
    InputAutocomplete,
  },
  data() {
    return {};
  },
  methods: {
    buttonClicked() {
      let location = this.$refs.inputautocompletefield.getSearch();
      console.log("search for location:", location);
    },
    userTypedLocation(location) {
      console.log("new location typed", location);
    },
    async getLocations() {
      let c = await jsonManager.getLocations();
      this.$refs.inputautocompletefield.updateItems(c);
    },
  },
  async mounted() {
    this.getLocations();

    this.$refs.inputautocompletefield.setPlaceholder("type location");
  },
};
</script>