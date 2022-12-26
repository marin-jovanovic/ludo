import {
    ContentCreator
} from "./content_creator.js";


// todo this can be made in more elegant way
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

        startState,
        startXY,

    }) {
        super();

        // todo find root cause of this
        startState = Number(startState);
        // startXY = Number(startXY);


        this.currentState = startState;
        this.currentXY = startXY;

        this.startState = startState;
        this.startXY = startXY;


        this.poolType = {
            pool: getConfig().pool["start"]
        }

    }

    get poolType() {
        return this.pool;
    }

    // set pool ({pool}) {
    set poolType({
        pool
    }) {

        if (!(pool in getConfig()["pool"])) {
            console.log("pool not exists", pool);
            return;
        }


        this.pool = pool;
    }

    moveTokenFromStartingPoolToLivePool = ({
        states
    }) => {
        // todo dehardcode absolute state

        this.poolType = {
            pool: getConfig().pool["live"]
        }


        // todo dehardcode, should be first state in live states
        this.currentState = 0;
        this.currentXY = states[this.currentState];

    }


    getObjectMaxKey(obj) {
        return Number(Object.keys(obj).reduce((a, b) => obj[a] > obj[b] ? a : b));
    }

    isAtDestination(states) {
        return this.currentState === this.getObjectMaxKey(states);
    }

    restart() {
        /**
         * one enemy token eats this token; move it to start position
         */

        this.currentState = this.startState;
        this.currentXY = this.startXY;
    }

    move = ({
        count,
        states
    }) => {
        this.currentState += count;
        this.currentXY = states[this.currentState];

    }

}


export {
    BlToken,
    getConfig
}