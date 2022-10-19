<template>
  <BaseNotification ref="notification"></BaseNotification>
  <div>
    <form @submit.prevent="addLocation">
      <CSRFToken ref="csrf"></CSRFToken>

      <div v-if="error" class="alert alert-danger">{{ error }}</div>

      <ui-textfield
        fullwidth
        v-model="name"
        helper-text-id="my-text-field-helper-text"
      >
        Name
      </ui-textfield>
      <br />
      <br />
      <ui-textfield
        fullwidth
        v-model="section"
        helper-text-id="my-text-field-helper-text"
      >
        Section
      </ui-textfield>

      <br />
      <br />
      <ui-textfield
        fullwidth
        v-model="type"
        helper-text-id="my-text-field-helper-text"
      >
        Type
      </ui-textfield>
      <br />
      <br />
      <section>
        <ui-select fullwidth :options="options" v-model="portfolio">
          Portfolio
        </ui-select>
      </section>

      <br />
      <div class="row">
        <div class="col">
          <button :disabled="loading" class="btn btn-primary">Add</button>
        </div>
      </div>
    </form>
    <br />
    <br />

    <div class="col">
      <button class="btn btn-primary" @click="clearForm">Clear</button>
    </div>
  </div>
</template>

<script>
import { apiPortfolio } from "@/scripts/api/portfolio";
import { apiLocation } from "../scripts/api/location";
import CSRFToken from "@/components/CSRFToken.vue";
import BaseNotification from "./BaseNotification.vue";

export default {
  emits: ["added", "closePopup"],
  data() {
    return {
      options: [],
      portfolio: "",
      name: "",
      section: "",
      type: "",

      submitted: false,
      loading: false,
      error: undefined,
    };
  },
  async mounted() {
    await this.getPortfolios();
  },
  methods: {
    async handleSubmit() {
      //     "Only letters, numbers, spaces, commas and dots accepted in the input",
      //   validationRegex: /^(\w|,|\.| )*$/,

      let t = this.$store.getters.clickedLocation;

      if (!t) {
        this.error = "Select location";
        this.$refs.notification.showMessage(
          false,
          undefined,
          "Select location"
        );

        return;
      }

      this.submitted = true;
      this.error = "";

      if (!(this.section && this.type && this.portfolio)) {
        this.error += "fill all fields";
      }
      if (!(t.latitude && t.longitude)) {
        this.error += "\nselect location";
      }

      // todo check portfolio
      const csrfToken = this.$store.getters.synchronizerToken;

      if (!csrfToken) {
        alert("error with auth, reloading");
        this.$refs.notification.showMessage(
          false,
          undefined,
          "Authentication failed! Reloading"
        );

        this.$router.go();
      }

      if (this.error) {
        return;
      }

      let r = await apiLocation.addLocation(
        this.portfolio,
        this.name,
        this.section,
        this.type,
        t.latitude,
        t.longitude,
        csrfToken
      );

      if (r.payload.status) {
        console.log("add ok, notify");
        this.$emit("added");
      } else {
        console.log("add err");
        this.error =
          "adding error, try new section/portfolio, maybe this exist";
      }

      this.$refs.notification.showMessage(
        r.payload.status,
        "Location added successfully!",
        "Location adding failed!"
      );

      this.clearForm();
      await this.$refs.csrf.refresh();
      this.submitted = false;
      this.$emit("closePopup");
    },
    addLocation() {
      console.log("add location", this.section, this.type, this.portfolio);
      this.handleSubmit();
    },
    clearForm() {
      this.section = "";
      this.type = "";
    },
    onSelected(selected) {
      this.selected = selected.value;
    },
    transformForSelection(p) {
      let t = [];
      for (const value of Object.values(p)) {
        t.push({ label: value.name, value: value.name });
      }

      return t;
    },
    async getPortfolios() {
      let r = await apiPortfolio.getPortoflios();
      if (r["auth"]["status"]) {
        let pl = r["payload"]["portfolios"];

        this.options = this.transformForSelection(pl);
      }

      return undefined;
    },
  },
  components: {
    CSRFToken,
    BaseNotification,
  },
};
</script>

<style>
</style>