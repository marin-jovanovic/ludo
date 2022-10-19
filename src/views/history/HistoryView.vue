<template>
  <BaseUserTemplate ref="nav">
    <div>
      <!-- history view -->

      <!-- <div class="row" v-for="r in rows" :key="r">
            <div class="col" v-for="c in cols" :key="c">
                <ColourCard></ColourCard>

            </div>

        </div> -->

      <div class="row">
        <div class="col" v-for="i in colours" :key="i">
          <input
            @click.prevent="colourClicked"
            type="color"
            class="form-control form-control-color"
            value="#f1aaf1"
          />
          revert to me
        </div>
      </div>

      <!--  -->
      <div class="col">
        <!-- <div class="col">
                <input @click.prevent="colourClicked" type="color" class="form-control form-control-color"
                    value="#f1aaf1">
                <hr>
            </div> -->

        <div class="row">
          <input type="text" v-model="colourHex" />
          <button @click="addColour">add colour</button>
          <hr />
        </div>

        <div class="row">
          <button @click="refresh">refresh</button>
          current state
          <br />
          <div v-for="i in colours" :key="i">
            {{ i }}
          </div>
          <hr />
        </div>

        <div class="row">
          <button @click="deleteAll">clear list</button>
          <hr />
        </div>
      </div></div
  ></BaseUserTemplate>
</template>
  

<script>
import { apiColour } from "../../scripts/api/colour";
import BaseUserTemplate from "@/components/BaseUserTemplate.vue";

export default {
  data() {
    return {
      colourHex: "#p",
      colours: ["a", "b"],
      rows: ["row1", "row2", "row3"],
      cols: ["col1", "col2", "col3"],
    };
  },
  mounted() {
    // this.$refs.nav.setActive("history");
  },
  methods: {
    colourClicked() {
      console.log("colour clicked");
    },
    async deleteAll() {
      console.log("delete all");
      let r = await apiColour.deleteColour("a");
      console.log(r);
    },
    async refresh() {
      let r = await apiColour.getAllColours("portfolio_1");
      console.table(r["payload"]["value"]);
      this.colours = [];
      for (const [key, value] of Object.entries(r["payload"]["values"])) {
        console.log(key, value, typeof key);
        this.colours.push(value);
      }
    },
    async addColour() {
      console.log(this.colourHex);
      console.log("add c");
      let r = await apiColour.addColour("a", this.colourHex);
      console.log(r);
    },
  },
  components: { BaseUserTemplate },
};
</script>
  