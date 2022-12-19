import {
    ContentCreator
} from "./content_creator.js";
import {
    remapPosition
} from "./ui_comm.js";
import {
    BoardTile
} from "./ui_board_tile.js";

/**
 * ===>>>
 * bl fires "bl token state updated"
 * bl sets flag that he sent info that something is updated
 * he will not fire another event until someone sends event back
 * 
 * this hints ui to update tokens position
 * 
 * <<<===
 * ui moves token to destination position
 * ui fires "ui token updated"
 * 
 * bl now knows that someone is listening
 * bl now knows that he can send another update/event 
 * 
 * -------------
 * bl has stack in which he keeps change log
 * when he can fire he will pop oldest change from stack and fire it
 * 
 * 
 */

class UiToken extends ContentCreator {

    constructor({
        position,
        colour
    }) {
        super();

        // x, y
        this.position = position;
        // todo determine (if game mode all_at_same_place then you know) else one by one
        // what if second is faster then this first one, still undetermined, this must update depending which ends first 

        // this.destinationPosition = position;

        this.radius = 8
        this.colour = colour;
        this.startingPosition = {
            x: position.x,
            y: position.y
        };

        // for jumping between tiles
        this.backlog = [];
        this.backlogSleepFrameCount = 10;
        this.backlogSleepFrameDec = 0;
        this.startSleeping = false;

        // todo extract to config
        // for jumping; sleep on each tile between start end destination tile
        // one by one
        this.configSleep = true;

        // move one by one tile (no diagonal => rather use first x then y ie)
        // prevent diagonals
        this.configOneByOne = true;

        this.choice_oneByOne_pythagoras = true;

        // this.previousPosition = undefined;

    }

    // todo this is rewired to setdestination
    restart = ({ position }) => {
        /**
         * one enemy token eats this token; move it to start position
         */

        console.log('restart catch')

        this.setDestionationPosition({
            diff: [position]
        })

    }

    setDestionationPosition = ({
        diff
    }) => {

        if (this.isBacklogEmpty()) {
            // todo improve by making this list and appending this list(diff)

            diff.forEach(i => {
                if (!("row" in i)) {
                    console.log("misssing row")
                }

                if (!("column" in i)) {
                    console.log("missing column")
                }

            })

            const clone = structuredClone(diff);
            this.backlog = clone;

        } else {
            console.log("err backlog load");
        }

        // this.getNextDestination();

    }


    isBacklogEmpty = () => {

        if (this.backlog === []) {
            console.log('init')
            return true;
        }

        if (!this.backlog) {
            console.log('indefind')
            return true;
        }

        if (!this.backlog.length === 0) {
            console.log('len 0')
            return true;
        }



        if (!this.backlog?.length != (this.backlog.length === 0)) {
            console.log('not same')
        }

        return !this.backlog?.length;

    }

    _sleep = () => {
        if (
            this.backlogSleepFrameDec === this.backlogSleepFrameCount
        ) {

            this.startSleeping = false;
            this.backlogSleepFrameDec = 0;

        } else {

            this.backlogSleepFrameDec += 1;

        }

    }

    getNextDestination = () => {

        if (this.isBacklogEmpty()) {
            console.log('err backlog empty, check before fetching');
            return;
        }

        console.log("ret value")
        return this.backlog[0];

    }


    _moveByOneToDestination = () => {

        if (this.isBacklogEmpty()) {
            console.log('at destination');
            return;
        }

        let destination = this.getNextDestination();

        // if ("row" in destination) {
        //     console.log("has row")
        // }

        // if (destination === false) {
        //     console.log("destination is false");
        // }

        if (!destination) {
            console.log(this.backlog)
            // console.log('destination undefined');
            return;
        }

        // console.log(destination)

        let des = remapPosition({
            i: destination.row,
            j: destination.column,
            Boundary: BoardTile
        });

        let atNextDestination = true;

        ['x', 'y'].forEach(i => {

            if (this.position[i] !== des[i]) {
                atNextDestination = false;

                if (this.position[i] > des[i]) {
                    this.position[i]--;
                } else if (this.position[i] < des[i]) {
                    this.position[i]++;
                }

            }
        })

        return atNextDestination;
    }

    draw = (c) => {
        c.beginPath();
        c.arc(
            this.position.x,
            this.position.y,
            this.radius,
            0,
            Math.PI * 2,
        );

        /**
         * check if at destination
         * 
         * if at destination
         * 
         * else
         * move in one increment towards destination
         * 
         * 
         * 
         */

        let wasAtDestination = this.isBacklogEmpty();

        if (!wasAtDestination) {

            if (this.configOneByOne) {
                if (this.configSleep && this.startSleeping) {
                    this._sleep();
                } else {

                    let atNextDestination = this._moveByOneToDestination();

                    if (atNextDestination) {
                        this.backlog.shift();

                        this.startSleeping = true;
                    }

                }
            } else {
                this._moveByOneToDestination();
            }
        }

        let isAtDestination = this.isBacklogEmpty();

        if (!wasAtDestination && isAtDestination) {
            // check if after redraw the token will be at the destination
            // if the token is at the destination then notify

            console.log("notify");
            this.notify({
                command: "UiUpdated"
            });
        }

        c.fillStyle = this.colour;
        c.fill();
        c.closePath();


    }

}

export {
    UiToken
}