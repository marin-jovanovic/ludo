import { ludo } from "./index.js";


class Token {
    constructor({ position, colour, state }) {
        this.startingPosition = { x: position.x, y: position.y };
        this.position = position;

        // separate business logic from view
        this.radius = 8

        // where is token on the board
        this.startingState = state
        this.state = state

        this.colour = colour;

        this.destinationPosition = position;

        // for jumping between tiles
        this.backlog = [];
        this.backlogSleepFrameCount = 10;
        this.backlogSleepFrameDec = 0;
        this.startSleeping = false;

        // todo extract to config
        // for jumping; sleep on each tile between start end destination tile
        this.configSleep = true;

    }

    restart() {
        this.state = this.startingState;

        this.setDestionationPosition(
            { x: this.startingPosition.x, y: this.startingPosition.y }
        )
    }

    setDestionationPosition(destinationPosition) {
        this.destinationPosition = destinationPosition;
    }

    moveByOne({ destinationPosition }) {
        this.backlog.push(destinationPosition);
    }

    _isAtDestination() {
        return this.backlog === [];
    }

    _isBacklogEmpty() {
        return this.backlog === [];
    }

    _getDestinationByOne() {
        if (this._isBacklogEmpty()) {
            // return [false, NaN];
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

    draw(c) {
        c.beginPath()
        c.arc(
            this.position.x,
            this.position.y,
            this.radius,
            0,
            Math.PI * 2,
        );

        let wasAtDestination = this._isAtDestination();

        if (!wasAtDestination) {
            if (this.configSleep && this.startSleeping) {
                this._sleep();
            } else {
                let nextDestination = this._getDestinationByOne();

                if (this._isBacklogEmpty()) {
                    console.log('intgr err')
                } else {
                    if (nextDestination) {
                        let atNextDestination = true;

                        ['x', 'y'].forEach(i => {

                            if (this.position[i] !== nextDestination[i]) {
                                atNextDestination = false;

                                if (this.position[i] > nextDestination[i]) {
                                    this.position[i]--;
                                } else if (this.position[i] < nextDestination[i]) {
                                    this.position[i]++;
                                }
                            }
                        })

                        if (atNextDestination) {
                            this.backlog.shift();

                            this.startSleeping = true;

                        }
                    }
                }



            }
        }

        let isAtDestination = this._isAtDestination();

        if (!wasAtDestination && isAtDestination) {
            // check if after redraw the token will be at the destination
            // if the token is at the destination then notify
            ludo.notify();
        }

        c.fillStyle = this.colour
        c.fill()
        c.closePath()
    }

}

export { Token }