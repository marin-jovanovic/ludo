<template>
  <w-drawer
    v-model="openDrawer"
    push-content
    :overlay-opacity="0.15"
    left
    width="160px"
  >
    <template #pushable>
      <w-flex class="py12" column align-center justify-center>
        <p class="mb3">Pushable content</p>
        <w-button @click="openDrawer = true" outline> Open drawer </w-button>
      </w-flex>
    </template>

    <div class="ma2">Drawer content</div>
  </w-drawer>
</template>

<script>
export default {
  data() {
    return {
      openDrawer: false,
    };
  },
  mounted() {
    console.log("l d mounted");
  },
};
</script>

<style>
</style>