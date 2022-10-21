<template>
  <div></div>
</template>
  
  <script>
import { useToast } from "vue-toastification";

export default {
  setup() {
    const toast = useToast();
    // toast("notif test");
    return { toast };
  },
  data() {
    return {};
  },
  methods: {
    showMessage(result, successMessage, errorMessage) {
      if (result) {
        if (successMessage) {
          this.toast.success(successMessage, {
            timeout: 2000,
          });
        }
      } else {
        if (errorMessage) {
          this.toast.error(errorMessage, {
            timeout: 2000,
          });
        }
      }
    },
  },
};
</script>
  