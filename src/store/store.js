import {
    createStore
} from 'vuex'

// this.$store.dispatch("setPath", value);
// let curr = this.$store.getters[variable];


export const store = createStore({
    state() {
        return {

            username: "",
            path: {},
        }
    },
    actions: {
        setPath(context, path) {
            context.commit("SET_PATH", path);
        },
        setUsername(context, username) {
            context.commit("SET_USERNAME", username);
        },
    },
    mutations: {
        SET_PATH(context, path) {
            console.log("set p", path)
            context.path = path;
        },
        SET_USERNAME(context, username) {
            context.username = username;
        },
    },
    getters: {
        path(state) {
            return state.path;
        },
        username(state) {
            return state.username;
        },
    }
})