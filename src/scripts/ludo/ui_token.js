import {
    ContentCreator
} from "./content_creator.js";
import {
    remapPosition
} from "./ui_comm.js";
import {
    BoardTile
} from "./ui_board_tile.js";
// import { circleCollidesWithPoint } from "./collisions.js";

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

        this.collides = false;
        this.colourCollides = "white";

        this.startingPosition = {
            x: position.x,
            y: position.y
        };

        // for jumping between tiles
        this.backlog = [];
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

        // todo expose
        // control how much time is spent on updating
        this.backlogSleepFrameCount = 2;
        this.increment = 12;


        this.occurances = 7;








    }

    set number({
        c
    }) {
        this.occurances = c;
    }

    setDestionationPosition = ({
        diff
    }) => {

        // console.log(diff)

        if (this.isBacklogEmpty()) {
            // todo improve by making this list and appending this list(diff)

            diff.forEach(i => {
                if (!("row" in i)) {
                    console.log("err: misssing row")
                }

                if (!("column" in i)) {
                    console.log("err: missing column")
                }

            })

            const clone = structuredClone(diff);
            this.backlog = clone;

        } else {
            console.log("err backlog load");
        }


    }


    isBacklogEmpty = () => {

        if (this.backlog === []) {
            console.log('err init')
            return true;
        }

        if (!this.backlog) {
            console.log('err indefind')
            return true;
        }

        if (!this.backlog.length === 0) {
            console.log('err len 0')
            return true;
        }



        if (!this.backlog?.length != (this.backlog.length === 0)) {
            console.log('err not same')
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

        return this.backlog[0];

    }


    _moveByOneToDestination = () => {

        if (this.isBacklogEmpty()) {
            console.log('at destination');
            return;
        }

        let destination = this.getNextDestination();

        if (!destination) {
            console.log(this.backlog)
            return;
        }


        let des = remapPosition({
            i: destination.row,
            j: destination.column,
            Boundary: BoardTile
        });

        let atNextDestination = true;

        /**
         * default speed is to move in increments by 1
         * that is referent speed of 100 %
         * 
         * 150% speed is increments of 1.50
         * 
         * 235% = 2.35
         * 
         * 85% = 0.85
         * 
         * add in increments 
         * ie 
         * start 2
         * target 7
         * 2    + 2.35 = 4.35
         * 4.35 + 2.35 = 6.70
         * 6.70 + 2.35 = over 7 (target), add only .30
         * 
         * start 7
         * target 2
         * 7    - 2.35 = 4.65
         * 4.65 - 2.35 = 2.30
         * 2.30 - 2.35 = less then 2, subtract only .30
         * 
         */


        ['x', 'y'].forEach(i => {

            if (this.position[i] !== des[i]) {

                atNextDestination = false;

                if (this.position[i] > des[i]) {

                    if (this.position[i] - this.increment < des[i]) {
                        this.position[i] = des[i];
                    } else {
                        this.position[i] -= this.increment;
                    }

                } else if (this.position[i] < des[i]) {

                    if (this.position[i] + this.increment > des[i]) {
                        this.position[i] = des[i];
                    } else {
                        this.position[i] += this.increment;
                    }

                }

            }
        })

        return atNextDestination;
    }

    draw = (c) => {





        c.font = "30px Arial";
        c.fillStyle = "white"
        c.fillText(String(this.occurances), this.position.x, this.position.y);

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

            this.notify({
                command: "UiUpdated"
            });
        }

        //         this.collides = false;
        // this.colourCollides = "white";

        if (this.collides) {
            c.fillStyle = this.colourCollides;

        } else {
            c.fillStyle = this.colour;

        }



        // if (circleCollidesWithPoint({circle: this, point: mousePosition})) {



        //     console.log("colliding")

        // }
        c.fill();
        c.closePath();

    }

}

export {
    UiToken
}