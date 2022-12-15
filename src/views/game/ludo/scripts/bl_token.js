import {
    ContentCreator
} from "./content_creator.js";



function getConfig() {
    let poolTypes = {

        // in starting pool
        "start": "start",

        // in game
        "live": "live",

        // reached destination position 
        "done": "done",
    }

    return {
        "pool": poolTypes,
    }
}


class BlToken extends ContentCreator {

    constructor({
        state
    }) {
        super();

        // relative numbers
        this.startingState = state;
        this.state = state;

        // absolute
        this.absoluteState = state;


        this.pool = getConfig()["pool"]["start"];
    }

    getObjectMaxKey(obj) {
        return Number(Object.keys(obj).reduce((a, b) => obj[a] > obj[b] ? a : b));
    }

    isAtDestination(states) {
        return this.state === this.getObjectMaxKey(states);
    }

    restart() {
        /**
         * one enemy token eats this token; move it to start position
         */

        // console.log("restart")

        // console.log(this.startingState);

        this.state = this.startingState;
        this.absoluteState = this.state;


        this.notify({
            command: "restart"
        });

    }

    move = ({
        count
    }) => {
        this.state += count;
        this.absoluteState += count;
    }

}


export {
    BlToken,
    getConfig
}