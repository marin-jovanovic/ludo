<template>
  <div class="col">
    <input
      type="color"
      class="form-control form-control-color"
      value="this.colour"
    />
  </div>
</template>
    
    <script>
export default {
  props: {
    colour: String,
  },
  data() {
    return {
      //   colour: "#259854",
    };
  },
  mounted() {
    console.log("mounted color", this.colour);
  },
  methods: {},
};
</script>
    