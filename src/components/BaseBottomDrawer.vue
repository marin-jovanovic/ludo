<template>
  <w-drawer v-model="isOpened" bottom>
    <div class="container-fluid">
      <div class="row">
        <div class="col">
          <div class="row">
            <div>
              portfolio
              <div id="example-3">
                <hr />
                <button @click="onChange">click to filter</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </w-drawer>
</template>

<script>
// import { apiPortfolio } from "@/scripts/api/portfolio";

export default {
  data() {
    return {
      isOpened: false,
      portfolios: undefined,
    };
  },
  //   methods: {
  //     openDrawer() {
  //       console.log("open");
  //       this.isOpened = true;
  //     },
  //     closeDrawer() {
  //       console.log("close");
  //       this.isOpened = false;
  //     },
  //     async fetchLocations() {
  //       let r = await apiPortfolio.getPortoflios();
  //       if (r["auth"]["status"]) {
  //         let pl = r["payload"]["portfolios"];

  //         for (const [key, value] of Object.entries(pl)) {

  //           let r = (await apiLocation.getAllLocationsInPortfolio(value.name))
  //             .payload.content;

  //         }
  //       }
  //     },
  //   },
};
</script>

<style>
</style>