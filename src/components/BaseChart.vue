<template>
  <div class="col">
    <apexchart
      width="500"
      type="area"
      :options="chartOptions"
      :series="series"
    ></apexchart>
    <div>
      <button @click="updateChart">Update</button>
    </div>
  </div>
</template>
  
  <script>
import { apiConsumption } from "@/scripts/api/consumption";
import { apiTemperature } from "@/scripts/api/temperature";
import VueApexCharts from "vue3-apexcharts";
export default {
  props: {
    portfolio: String,
    section: String,
    type: String,
  },
  name: "GraphIndex",
  data() {
    return {
      chartOptions: {
        chart: {
          id: "vuechart-example",
        },
        xaxis: {
          categories: [],
        },
      },
      series: [
        {
          name: "series-1",
          data: [2, 91],
        },
      ],

      location: undefined,
    };
  },
  components: { apexchart: VueApexCharts },
  computed: {
    defaultData() {
      return {
        // labels: [],
        labels: ["months", "a", "b", "c", "d", "e", "f", "g"],
        datasets: [
          {
            label: "Data One",
            backgroundColor: "rgb(228,102,81,0.9)",
            data: [10, 10, 10, 50, 30, 70, 35],
          },
          {
            label: "Data Two",
            backgroundColor: "rgb(0,216,255,0.9)",
            data: [39, 80, 40, 35, 40, 20, 45],
          },
        ],
      };
    },
  },
  async mounted() {
    console.log("mounted base chart");
  },

  methods: {
    async fetchConsumption(portfolio, section, type) {
      let r = await apiConsumption.getAllConsumption(portfolio, section, type);

      if (r["payload"]["status"]) {
        let values = r["payload"]["result"];
        if (!values) {
          console.log("no values for this location");
          return;
        }

        this.chartOptions = {
          chart: {
            id: "temperature",
          },
          xaxis: {
            categories: Object.keys(values),
          },
        };

        this.series = [
          {
            data: Object.values(values),
          },
        ];
      } else {
        console.log("error fetching");
        // this.showMessage(false, "", "Error fetching data, contact admin");
      }
    },
    async fetchTemperature(portfolio, section, type) {
      console.log("get temp");

      let r = await apiTemperature.getAllTemperature(portfolio, section, type);

      if (r["payload"]["status"]) {
        let values = r["payload"]["result"];
        if (!values) {
          console.log("no values for this location");
          return;
        }

        this.chartOptions = {
          chart: {
            id: "temperature",
          },
          xaxis: {
            categories: Object.keys(values),
          },
        };

        this.series = [
          {
            data: Object.values(values),
          },
        ];
      } else {
        console.log("error fetching");
        // this.showMessage(false, "", "Error fetching data, contact admin");
      }
    },
  },
};
</script>
  