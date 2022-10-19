<template>
  <input hidden :value="content" @change="updateMyValue" />
</template>

<script>
import { apiCsrf } from "../scripts/api/csrf";

export default {
  data() {
    return {
      content: "",
    };
  },
  async mounted() {
    this.refresh();
  },
  methods: {
    async refresh() {
      const r = await apiCsrf.getCSRFAuthData();
      if (r["auth"]["status"]) {
        this.content = r["payload"]["synchronizer_token"];
      } else {
        this.content = "";

        alert(
          "error generating SynchronizerToken, you will not be able to submit form, contact admin"
        );
      }

      this.$store.dispatch("setSynchronizerToken", this.content);
    },

    updateMyValue(event) {
      this.content = event.target.value.trim();
      this.$store.dispatch("setSynchronizerToken", this.content);
    },
  },
};
</script>
