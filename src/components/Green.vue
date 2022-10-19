<template>
  <div v-show="timerCount !== 0">
    <div class="alert alert-success" role="alert">
      {{ this.content }} {{ timerCount }}
    </div>
  </div>
</template>
  

  <script>
export default {
  name: "GreenBanner",
  props: {
    customContent: String,
  },
  data() {
    return {
      content: this.customContent,
      timerCount: 0,
    };
  },

  methods: {
    setContent(content) {
      this.content = content;
    },
    show() {
      this.timerCount = 3;
    },
  },

  watch: {
    timerCount: {
      handler(value) {
        if (value > 0) {
          setTimeout(() => {
            this.timerCount--;
          }, 1000);
        }
      },
      immediate: true,
    },
  },
};
</script>
  