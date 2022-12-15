import App from './App.vue'
import {
    router
} from './router/router';
import {
    store
} from "./store/store"
import OpenLayersMap from 'vue3-openlayers'
import 'vue3-openlayers/dist/vue3-openlayers.css'
import WaveUI from 'wave-ui'
import 'wave-ui/dist/wave-ui.css'
import BalmUI from 'balm-ui';
import BalmUIPlus from 'balm-ui/dist/balm-ui-plus';
import {
    createApp
} from 'vue/dist/vue.esm-bundler';
import VueSweetalert2 from 'vue-sweetalert2';
import 'sweetalert2/dist/sweetalert2.min.css';
import Toast from "vue-toastification";
import "vue-toastification/dist/index.css";

const app = createApp(App)
const sts = require('strict-transport-security');
const globalSTS = sts.getSTS({
    'max-age': {
        'days': 10
    },
    'includeSubDomains': true
});

new WaveUI(app, {})

app.use(VueSweetalert2);
app.use(Toast, {
    transition: "Vue-Toastification__bounce",
    maxToasts: 20,
    newestOnTop: true
});
app.use(BalmUI);
app.use(BalmUIPlus);
app.use(store);
app.use(router)
app.mount('#app');
app.use(OpenLayersMap, globalSTS);