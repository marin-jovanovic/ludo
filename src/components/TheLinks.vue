<template>
  <div class="misc">
    <a class="small text-muted">
      <router-link :to="{ name: 'signup' }">signup</router-link>
    </a>

    <br />
    <a class="small text-muted">
      <router-link :to="{ name: 'login' }">login</router-link>
    </a>
    <br />
  </div>
</template>

<script>
export default {
  name: "loginLinks",
  props: {
    sentUsername: String,
  },
  data() {
    return {
      username: "",
    };
  },
  async mounted() { },
  methods: {
    usernameChange() {
      // $emit('getUsername');
      console.log("sent username", this.sentUsername);
      this.$store.dispatch("setUsername", this.username);
    },
  },
};
</script>
