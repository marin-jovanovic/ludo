import {
    createStore
} from 'vuex'

// this.$store.dispatch("setPath", value);
// let curr = this.$store.getters[variable];


export const store = createStore({
    state() {
        return {

            // todo, this is in .env
            appMode: "development",

            clickedLocation: undefined,

            map: undefined,

            location: undefined,

            charts: [],

            zoomUserLocation: false,

            // user coordinates
            userCoordiantes: {},
            synchronizerToken: "",
            username: "",
            path: {},
        }
    },
    actions: {
        setPath(context, path) {
            context.commit("SET_PATH", path);
        },
        setUserCoordinates(context, userCoordiantes) {
            context.commit("SET_USER_COORDINATES", userCoordiantes);

        },
        setSynchronizerToken(context, synchronizerToken) {
            context.commit("SET_SYNCHRONIZER_TOKEN", synchronizerToken);
        },
        setUsername(context, username) {
            context.commit("SET_USERNAME", username);
        },
        setMap(context, map) {
            context.commit("SET_MAP", map);
        },

        setZoomUserLocation(context, zoomUserLocation) {
            context.commit("SET_ZOOM_USER_LOCATION", zoomUserLocation);
        },
        setClickedLocation(context, clickedLocation) {
            context.commit("SET_CLICKED_LOCATION", clickedLocation);

        }

    },
    mutations: {
        SET_PATH(context, path) {
            console.log("set p", path)
            context.path = path;
        },
        SET_USER_COORDINATES(context, userCoordiantes) {
            context.userCoordiantes = userCoordiantes;
        },
        SET_USERNAME(context, username) {
            context.username = username;
        },
        SET_SYNCHRONIZER_TOKEN(state, synchronizerToken) {
            state.synchronizerToken = synchronizerToken;
        },
        SET_ZOOM_USER_LOCATION(state, zoomUserLocation) {
            state.zoomUserLocation = zoomUserLocation
        },
        SET_CLICKED_LOCATION(state, clickedLocation) {
            state.clickedLocation = clickedLocation;
        },
        SET_MAP(state, map) {
            state.map = map;
        },

        SELECT_LOCATION(state, location) {
            state.location = location;
        },
        ADD_CHART(state, chart) {
            state.charts.push(chart);
        }
    },
    getters: {
        path(state) {
            return state.path;
        },
        coordiantes(state) {
            return state.coordiantes
        },
        synchronizerToken(state) {
            return state.synchronizerToken;
        },
        username(state) {
            return state.username;
        },
        map(state) {
            return state.map;
        },

        location(state) {
            return state.location;
        },
        charts(state) {
            return state.charts;
        },
        zoomUserLocation(state) {
            return state.zoomUserLocation;
        },
        clickedLocation(state) {
            return state.clickedLocation;
        },

    }

})