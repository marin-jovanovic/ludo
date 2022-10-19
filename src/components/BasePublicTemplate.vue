<template>
  <canvas id="canvas1"></canvas>

  <section class="vh-100" style="background-image: url('assets/login_bg.jpg')">
    <div class="container py-5 h-100">
      <div class="row d-flex justify-content-center align-items-center h-100">
        <div class="col col-xl-10">
          <div class="card" style="border-radius: 1rem">
            <div class="row g-0">
              <div class="col-md-6 col-lg-5 d-none d-md-block">
                <img
                  src="assets/login_profile.jpg"
                  alt="login form"
                  class="img-fluid"
                  style="border-radius: 1rem 0 0 1rem"
                />
              </div>
              <div class="col-md-6 col-lg-7 d-flex align-items-center">
                <div class="card-body p-4 p-lg-5 text-black">
                  <div class="d-flex align-items-center mb-3 pb-1">
                    <span class="h1 fw-bold mb-0">
                      <img
                        src="assets/login_logo.png"
                        alt="img"
                        class="img-fluid float-left"
                      />
                    </span>
                  </div>
                  <slot />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style>
#canvas1 {
  border: 3px solid black;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  height: 100%;
  width: 100%;
}
</style>

<script>
// import { runClouds } from "../scripts/clouds";

export default {
  data() {
    return {};
  },
  mounted() {
    // runClouds();
  },
};
</script> 
