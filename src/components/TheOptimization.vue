<template>
  <div>
    {{ locations }}
    <br />
    <hr />
    <button @click="performOptimization">optimize selected</button>
  </div>
</template>

<script>
// import "http://ajax.googleapis.com/ajax/libs/jquery/1.7/jquery.min.js";
// import "https://cdn.jsdelivr.net/npm/sweetalert2@8";

export default {
  props: {
    locations: Object,
  },
  data() {
    return {};
  },
  mounted() {},
  methods: {
    performOptimization() {
      console.log("optimize with");
      console.log(this.locations);
      // todo make api call for this optimization and show message if optimization
      // this.$swal("Hello Vue world!!!");

      this.$swal.fire("Optimization done", "", "success");

      // todo refresh selection and graphs

      // this.$swal.fire({
      //   title: "Please Wait",
      //   allowEscapeKey: false,
      //   allowOutsideClick: false,
      //   background: "#19191a",
      //   showConfirmButton: false,
      //   onOpen: () => {
      //     this.$swal.showLoading();
      //   },

      //   // timer: 3000,
      //   // timerProgressBar: true
      // });

      // let timerInterval;
      // this.$swal
      //   .fire({
      //     title: "Auto close alert!",
      //     html: "I will close in <b></b> milliseconds.",
      //     timer: 2000,
      //     timerProgressBar: true,
      //     didOpen: () => {
      //       this.$swal.showLoading();
      //       const b = this.$swal.getHtmlContainer().querySelector("b");
      //       timerInterval = setInterval(() => {
      //         b.textContent = this.$swal.getTimerLeft();
      //       }, 100);
      //     },
      //     willClose: () => {
      //       clearInterval(timerInterval);
      //     },
      //   })
      //   .then((result) => {
      //     /* Read more about handling dismissals below */
      //     if (result.dismiss === this.$swal.DismissReason.timer) {
      //       console.log("I was closed by the timer");
      //     }
      //   });

      // this.$Swal.fire({
      //   title: "Error!",
      //   text: "Do you want to continue",
      //   icon: "error",
      //   confirmButtonText: "Cool",
      // });
    },
  },
};
</script>

<style>
@import "https://cdn.jsdelivr.net/npm/@sweetalert2/theme-dark@3";
</style>