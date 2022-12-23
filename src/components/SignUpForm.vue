<template>
  <form @submit.prevent="handleSubmit">
    <div v-if="error" class="alert alert-danger">{{ error }}</div>
    <div class="form-outline mb-4">
      <label class="form-label" for="form2Example17">Username</label>
      <input
        type="text"
        id="form2Example17"
        v-model="username"
        class="form-control form-control-lg"
        :class="{ 'is-invalid': submitted && !username }"
      />

      <div v-show="submitted && !username" class="invalid-feedback">
        Username is required
      </div>
    </div>

    <div class="form-outline mb-4">
      <label class="form-label" for="form2Example27">Password</label>

      <input
        type="password"
        id="form2Example27"
        v-model="password"
        :class="{ 'is-invalid': submitted && !password }"
        class="form-control form-control-lg"
      />

      <div v-show="submitted && !password" class="invalid-feedback">
        Password is required
      </div>
    </div>

    <div class="form-outline mb-4">
      <label class="form-label" for="form2Example27">Repeat password</label>

      <input
        type="password"
        id=""
        v-model="passwordRepeat"
        :class="{ 'is-invalid': submitted && !passwordRepeat }"
        class="form-control form-control-lg"
      />

      <div v-show="submitted && !password" class="invalid-feedback">
        Password is required
      </div>
    </div>

    <div class="pt-1 mb-4">
      <button class="btn btn-dark btn-lg btn-block" :disabled="loading">
        Sign up
      </button>
    </div>
  </form>
</template>
  
  
<script>
import { router } from "../router/router";
import { apiAuth } from "../scripts/api/auth";
export default {
  data() {
    return {
      username: "a",
      password: "a",
      passwordRepeat: "a",
      submitted: false,
      loading: false,
      returnUrl: "",
      error: "",
    };
  },
  created() {
    apiAuth.logout();
    this.returnUrl = this.$route.query.returnUrl || "/";
  },
  methods: {
    handleSubmit() {
      this.submitted = true;
      const { username, password } = this;

      if (!(this.username && this.password && this.passwordRepeat)) {
        this.error = "fill all the fields";
        return;
      }

      if (!(this.password === this.passwordRepeat)) {
        this.error = "passwords are not matching";
        return;
      }

      // this.loading = true;
      apiAuth.signup(username, password).then(
        () => {
          router.push(this.returnUrl);
          this.$store.dispatch("setUsername", username);
        },
        (error) => {
          this.error = "invalid credentials";
          this.error = error;
          this.loading = false;
        }
      );
    },
  },
};
</script> 
      