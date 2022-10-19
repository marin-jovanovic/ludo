<template>
  <BaseUserTemplate>
    <div class="row">
      <div class="col">
        <BaseChart :portfolio="portfolio" :p="chartOptions"></BaseChart>
      </div>
    </div>
  </BaseUserTemplate>
</template>
  
  <script>
import BaseChart from "@/components/BaseChart.vue";
import BaseUserTemplate from "@/components/BaseUserTemplate.vue";

export default {
  name: "GraphIndex",
  data() {
    return {
      chartOptions: {
        chart: {
          id: "vuechart-example",
        },
        xaxis: {
          categories: [1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998],
        },
      },

      portfolio: undefined,
      section: undefined,
      type: undefined,
    };
  },
  mounted() {
    console.log("moutned p");
    this.portfolio = this.$route.params.portfolio;
    this.section = this.$route.params.section;
    this.type = this.$route.params.type;
    console.log(this.portfolio, this.section, this.type);
  },
  components: { BaseChart, BaseUserTemplate },
};
</script>
  
