<template>
  <input
    class="form-check-input"
    type="checkbox"
    id="checkboxNoLabel"
    aria-label="..."
    v-model="isSelected"
    @change="checkboxChange(isSelected)"
  />
</template>

<script>
export default {
  props: {
    isSelectedInit: Boolean,
  },
  data() {
    return {
      isSelected: false,
    };
  },
  mounted() {
    console.log("setting", this.isSelectedInit);
    this.isSelected = this.isSelectedInit;
    console.log("t", this.isSelectedInit);
  },

  methods: {
    updateValue(isSelected) {
      this.isSelected = isSelected;
    },
    checkboxChange(isSelected) {
      this.$emit("checkboxChange", isSelected);
    },
  },
};
</script>

<style>
</style>