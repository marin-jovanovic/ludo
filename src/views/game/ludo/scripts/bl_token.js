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

    // console.log("get pool", poolTypes)

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
        startXY = Number(startXY);

        // console.log(startState, startXY)

        this.currentState = startState;
        this.currentXY = startXY;

        this.startState = startState;
        this.startXY =  startXY;

        // relative numbers
        this.startingState = startState;
        // natural number
        this.state = startState;

        // absolute
        // this.absoluteState = startState;

        // this is row/column position
        // start position
        this.boardXYPosition = startXY;


        this.xy = startXY;


        this.poolType = {
            pool: getConfig().pool["start"]
        }

    
        this.stateTraversal = undefined;
    }

    get poolType() {
        return this.pool;
    }

    moveTokenFromStartingPoolToLivePool = () => {
        console.log("move ")
        // todo dehardcode absolute state

        this.poolType = {
            pool: getConfig().pool["live"]
            // pool: getPoolType({type: "live"}) 
        }


        this.state = 0;

    }

    // set pool ({pool}) {
    set poolType ({pool}) {

        if (! (pool in getConfig()["pool"])) {
        console.log("pool not exists", pool);
        return;
        }


        this.pool = pool;
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

        this.state = this.startingState;
        // this.absoluteState = this.state;

    }

    move = ({
        count
    }) => {
        this.state += count;
        // this.absoluteState += count;
    }

}


export {
    BlToken,
    getConfig
}