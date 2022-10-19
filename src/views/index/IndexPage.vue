<template>
  <BaseUserTemplate>
    <div>index page</div>
  </BaseUserTemplate>
</template>

<script>
import { useToast } from "vue-toastification";
import BaseUserTemplate from "@/components/BaseUserTemplate.vue";

export default {
  setup() {
    const toast = useToast();
    toast("notif test");
    return { toast };
  },
  data() {
    return {
      notification: {
        show: false,
        position: ["bottom", "right"],
      },
    };
  },
  methods: {
    successNotify(content) {
      this.toast.success(content, {
        timeout: 2000,
      });
    },
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
    notify() {
      this.showMessage(false, "t", "f");
    },
  },
  components: { BaseUserTemplate },
};
</script>
