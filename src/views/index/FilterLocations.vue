<template>
    <div>
        portfolio
        <div id='example-3'>
            <div v-for="p in Object.keys(portfolios)" :key="p">
                <input type="checkbox" :id="p" :value="p" v-model="checkedNames">
                <label :for="p">{{ p }}</label>
                <hr>

            </div>
            <span>Checked portfolios: {{ checkedNames }}</span>
            <hr>
            <button @click="filterMarkers">click to filter</button>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            checkedNames: [],
            portfolios: []
        }
    },
    methods: {
        filterMarkers() {
            let portfolios = this.$store.getters.portfolios;
            let map = this.$store.getters.map;

            for (const value of Object.values(portfolios)) {
                value["visible"] = false;
                map.removeLayer(value["vectorLayer"]);
            }

            this.checkedNames.forEach(i => {
                portfolios[i]["visible"] = true
            })

            for (const value of Object.values(portfolios)) {
                if (value["visible"]) {
                    map.addLayer(value["vectorLayer"]);
                }
            }

            this.$store.dispatch("setMap", map);
            this.$store.dispatch("setPortfolios", portfolios);

        },
    }
}
</script>