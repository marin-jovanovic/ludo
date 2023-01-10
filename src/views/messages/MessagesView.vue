<template>
  <base-user-template>
    <div>
      <div id="wrapper">
        <div id="w30">
          <div>p</div>
        </div>
        <div id="w70">width 70%</div>
      </div>
    </div>
  </base-user-template>
</template>
      
    <script>
import BaseUserTemplate from "@/components/BaseUserTemplate.vue";

export default {
  data() {
    return { username: undefined, profilePhoto: undefined };
  },
  async mounted() {},
  components: {
    BaseUserTemplate,
  },
};
</script>
      
    <style>
#wrapper {
  display: flex;
  width: 100%;
}
#w30 {
  background: yellow;
  width: 30%;
}

#w70 {
  background: pink;
  width: 70%;
}
</style>