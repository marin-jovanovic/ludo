<template>
  <base-user-template>
    <div>waiting room level</div>
  </base-user-template>
</template>

<script>
import BaseUserTemplate from "@/components/BaseUserTemplate.vue";
export default {
  components: { BaseUserTemplate },
  data() {
    return {
      gameId: undefined,
    };
  },
  mounted() {
    this.gameId = this.$route.params.id;
    console.log(this.gameId);
  },
};
</script>

<style>
</style>
