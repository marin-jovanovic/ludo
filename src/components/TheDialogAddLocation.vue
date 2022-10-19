<template>
  <w-dialog
    v-model="dialog.show"
    :fullscreen="dialog.fullscreen"
    :width="dialog.width"
    :persistent="dialog.persistent"
    :persistent-no-animation="dialog.persistentNoAnimation"
    title-class="primary-light1--bg white"
  >
    <AddContent @added="addOk"></AddContent>
  </w-dialog>
</template>

<script>
import AddContent from "./AddContent.vue";
export default {
  data() {
    return {
      dialog: {
        show: false,
        fullscreen: false,
        persistent: false,
        persistentNoAnimation: false,
        width: 300,
      },
    };
  },
  methods: {
    addOk() {
      console.log("addd ok");
      this.closeDialog();
    },
    showDialog() {
      this.dialog.show = true;
    },
    closeDialog() {
      this.dialog.show = false;
    },
  },
  components: { AddContent },
};
</script>

<style>
</style>