<template>
  <div>
    <div class="container">
      <div class="left-div" style="width: 15%; float: left"></div>
      <div
        class="middle-div"
        style="width: 70%; float: left; border: 1px solid"
      >
        <slot />
      </div>
      <div class="right-div" style="width: 15%; float: left"></div>
    </div>
  </div>
</template>
          
<script>
export default {
  data() {
    return {};
  },
  async mounted() {},
  methods: {},
};
</script>

<style>
.container {
  display: flex;
  justify-content: space-between;
}
.left-div,
.middle-div,
.right-div {
  height: 100%;
}
</style>