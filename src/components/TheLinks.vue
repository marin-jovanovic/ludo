<template>
  <div class="misc">
    <a class="small text-muted">
      <router-link :to="{ name: 'login' }">home</router-link>
    </a>
    <br />
    <a class="small text-muted">
      <router-link @click="usernameChange()" :to="{ name: 'forgotpassword' }"
        >Forgot password?</router-link
      >
    </a>
    <br />
    <a class="small text-muted">
      <router-link :to="{ name: 'termsofuse' }">Terms of use</router-link>
    </a>
    <br />
    <a class="small text-muted">
      <router-link :to="{ name: 'privacypolicy' }">Privacy policy</router-link>
    </a>
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
  async mounted() {},
  methods: {
    usernameChange() {
      // $emit('getUsername');
      console.log("sent username", this.sentUsername);
      this.$store.dispatch("setUsername", this.username);
    },
  },
};
</script>
