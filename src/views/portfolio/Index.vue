<template>
  <BaseUserTemplate>
    <div class="container mt-2">
      <div class="row">
        <div class="col">
          <BasePortfolioList
            @selectUpdate="updateSelectedList"
            @increase-by="updateSelectedForChart"
            :selectedForChart="selected"
          ></BasePortfolioList>
        </div>
        <!-- <div class="col">
          <BaseChart ref="temperature"></BaseChart>
          <BaseChart ref="consumption"></BaseChart>

          <button @click="showSelected">show selected</button>
        </div> -->
      </div>

      <div class="row">
        <TheOptimization :locations="selectedList"></TheOptimization>
      </div></div
  ></BaseUserTemplate>
</template>


<script>
import BasePortfolioList from "@/components/BasePortfolioList.vue";
// import BaseChart from "@/components/BaseChart.vue";
import TheOptimization from "@/components/TheOptimization.vue";
import BaseUserTemplate from "@/components/BaseUserTemplate.vue";

export default {
  name: "PortfolioIndex",
  data() {
    return {
      selected: {},
      selectedList: {},
    };
  },
  mounted() {
    // console.log("mounted", this.selected);
  },
  methods: {
    // performOptimization() {
    //   console.log("optimize with");
    //   console.log(this.selectedList);
    // },
    updateSelectedList(pl) {
      console.log("checkobx tick", pl);
      console.log("base");

      let o = {
        portfolio: pl.portfolio,
        section: pl.locationPayload.oldSection,
        type: pl.locationPayload.oldType,
      };
      console.table(o);

      let isSelected = pl.locationPayload.isSelected;
      console.log(isSelected);

      if (!(o.portfolio in this.selectedList)) {
        console.log("new portfolio");
        this.selectedList[o.portfolio] = new Set();
      }

      if (isSelected) {
        this.selectedList[o.portfolio].add({
          section: o.section,
          type: o.type,
        });
      } else {
        this.selectedList[o.portfolio].delete({
          section: o.section,
          type: o.type,
        });
      }

      for (const [key, value] of Object.entries(this.selectedList)) {
        console.log(key);
        console.table(value);
      }
    },
    async updateSelectedForChart(pl) {
      console.log("pl ff cl", pl);

      let portfolio = pl.portfolio;
      let section = pl.section;
      let type = pl.type;

      await this.$refs.temperature.fetchTemperature(portfolio, section, type);
      await this.$refs.consumption.fetchConsumption(portfolio, section, type);
    },
    showSelected() {
      console.log(this.selected);
    },
  },
  components: {
    BasePortfolioList,
    // BaseChart,
    TheOptimization,
    BaseUserTemplate,
  },
};
</script> 
