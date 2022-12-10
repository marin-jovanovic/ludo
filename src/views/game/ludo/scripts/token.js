import { ContentCreator } from "./content_creator.js";

class UiToken extends ContentCreator {

    constructor({ position, colour, state }) {
        super();

        // business logic
        this.position = position;

        // where is token on the board
        this.startingState = state
        this.state = state

        this.destinationPosition = position;

        // user interface 
        this.radius = 8

        this.colour = colour;
        this.startingPosition = { x: position.x, y: position.y };

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

    }

    restart() {
        /**
         * one enemy token eats this token; move it to start position
         */

        this.state = this.startingState;

        this.setDestionationPosition(
            { x: this.startingPosition.x, y: this.startingPosition.y }
        )
    }

    setDestionationPosition(destinationPosition) {
        this.destinationPosition = destinationPosition;
    }

    moveByOne({ destinationPosition }) {

        console.log("move by one", destinationPosition)

        this.setDestionationPosition(destinationPosition)

        // this.backlog.push(destinationPosition);
    }

    _isBacklogEmpty() {
        return this.backlog.length === 0;
    }

    _getDestinationByOne() {
        if (this._isBacklogEmpty()) {
            console.log('integrity error');
            return
        }

        return this.backlog[0];
    }



    _moveByOneToDestination(des) {
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

    draw(c) {
        c.beginPath()
        c.arc(
            this.position.x,
            this.position.y,
            this.radius,
            0,
            Math.PI * 2,
        );

        this.notify({command: "token stopped"});


        let wasAtDestination = this._isBacklogEmpty();

        if (!wasAtDestination) {

            if (this.configOneByOne) {
                if (this.configSleep && this.startSleeping) {
                    this._sleep();
                } else {
                    
                    let atNextDestination = this._moveByOneToDestination(
                        this._getDestinationByOne()
                    );

                    if (atNextDestination) {
                        this.backlog.shift();

                        this.startSleeping = true;
                    }

                }
            } else {
                this._moveByOneToDestination(this.destinationPosition);
            }
        }

        let isAtDestination = this._isBacklogEmpty();

        if (!wasAtDestination && isAtDestination) {
            // check if after redraw the token will be at the destination
            // if the token is at the destination then notify
            
            console.log("notify")
            this.notify({command: "token stopped"});
        }

        c.fillStyle = this.colour
        c.fill()
        c.closePath()
    }

}

class Token extends ContentCreator {

    constructor({ position, colour, state }) {
        super();

        // business logic
        this.position = position;

        // where is token on the board
        this.startingState = state
        this.state = state

        this.destinationPosition = position;


        // user interface 
        this.radius = 8

        this.colour = colour;
        this.startingPosition = { x: position.x, y: position.y };

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

    }

    restart() {
        /**
         * one enemy token eats this token; move it to start position
         */

        this.state = this.startingState;

        this.setDestionationPosition(
            { x: this.startingPosition.x, y: this.startingPosition.y }
        )
    }

    setDestionationPosition(destinationPosition) {
        this.destinationPosition = destinationPosition;
    }

    moveByOne({ destinationPosition }) {

        console.log("move by one", destinationPosition)

        this.setDestionationPosition(destinationPosition)

        // this.backlog.push(destinationPosition);
    }

    _isBacklogEmpty() {
        return this.backlog.length === 0;
    }

    _getDestinationByOne() {
        if (this._isBacklogEmpty()) {
            console.log('integrity error');
            return
        }

        return this.backlog[0];
    }

    _sleep() {
        if (
            this.backlogSleepFrameDec === this.backlogSleepFrameCount
        ) {

            this.startSleeping = false;
            this.backlogSleepFrameDec = 0;

        } else {

            this.backlogSleepFrameDec += 1;

        }

    }

    _moveByOneToDestination(des) {
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

    draw(c) {
        // console.log("draw");
        c.beginPath()
        c.arc(
            this.position.x,
            this.position.y,
            this.radius,
            0,
            Math.PI * 2,
        );

        // let wasAtDestination = this._isBacklogEmpty();

        // if (!wasAtDestination) {
            this._moveByOneToDestination(this.destinationPosition);

        // }

        // if (!wasAtDestination) {

        //     if (this.configOneByOne) {
        //         if (this.configSleep && this.startSleeping) {
        //             this._sleep();
        //         } else {
                    
        //             let atNextDestination = this._moveByOneToDestination(
        //                 this._getDestinationByOne()
        //             );

        //             if (atNextDestination) {
        //                 this.backlog.shift();

        //                 this.startSleeping = true;
        //             }

        //         }
        //     } else {
        //         this._moveByOneToDestination(this.destinationPosition);
        //     }
        // }

        // let isAtDestination = this._isBacklogEmpty();

        // if (!wasAtDestination && isAtDestination) {
        //     // check if after redraw the token will be at the destination
        //     // if the token is at the destination then notify
            
        //     console.log("notify")
        //     this.notify({command: "token stopped"});
        // }

        c.fillStyle = this.colour
        c.fill()
        c.closePath()
    }

}

export { Token, UiToken }