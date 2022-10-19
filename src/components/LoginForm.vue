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

    <div class="pt-1 mb-4">
      <button class="btn btn-dark btn-lg btn-block" :disabled="loading">
        Login
      </button>

      <img
        v-show="loading"
        src="data:image/gif;base64,R0lGODlhEAAQAPIAAP///wAAAMLCwkJCQgAAAGJiYoKCgpKSkiH/C05FVFNDQVBFMi4wAwEAAAAh/hpDcmVhdGVkIHdpdGggYWpheGxvYWQuaW5mbwAh+QQJCgAAACwAAAAAEAAQAAADMwi63P4wyklrE2MIOggZnAdOmGYJRbExwroUmcG2LmDEwnHQLVsYOd2mBzkYDAdKa+dIAAAh+QQJCgAAACwAAAAAEAAQAAADNAi63P5OjCEgG4QMu7DmikRxQlFUYDEZIGBMRVsaqHwctXXf7WEYB4Ag1xjihkMZsiUkKhIAIfkECQoAAAAsAAAAABAAEAAAAzYIujIjK8pByJDMlFYvBoVjHA70GU7xSUJhmKtwHPAKzLO9HMaoKwJZ7Rf8AYPDDzKpZBqfvwQAIfkECQoAAAAsAAAAABAAEAAAAzMIumIlK8oyhpHsnFZfhYumCYUhDAQxRIdhHBGqRoKw0R8DYlJd8z0fMDgsGo/IpHI5TAAAIfkECQoAAAAsAAAAABAAEAAAAzIIunInK0rnZBTwGPNMgQwmdsNgXGJUlIWEuR5oWUIpz8pAEAMe6TwfwyYsGo/IpFKSAAAh+QQJCgAAACwAAAAAEAAQAAADMwi6IMKQORfjdOe82p4wGccc4CEuQradylesojEMBgsUc2G7sDX3lQGBMLAJibufbSlKAAAh+QQJCgAAACwAAAAAEAAQAAADMgi63P7wCRHZnFVdmgHu2nFwlWCI3WGc3TSWhUFGxTAUkGCbtgENBMJAEJsxgMLWzpEAACH5BAkKAAAALAAAAAAQABAAAAMyCLrc/jDKSatlQtScKdceCAjDII7HcQ4EMTCpyrCuUBjCYRgHVtqlAiB1YhiCnlsRkAAAOwAAAAAAAAAAAA=="
      />
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
      if (!(username && password)) {
        return;
      }
      this.loading = true;
      apiAuth.login(username, password).then(
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
    
    