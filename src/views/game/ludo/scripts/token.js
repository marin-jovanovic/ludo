import { ludo } from "./index.js";


class Token {
    constructor({ position, colour, state }) {
        this.startingPosition = {x: position.x, y: position.y};
        this.position = position;
        
        this.radius = 8

        // where is token on the board
        this.startingState = state
        this.state = state

        this.colour = colour;

        this.destinationPosition = position;

        // this.backlog = [];
    
    }

    restart() {

        this.state = this.startingState;

        this.setDestionationPosition(
            {x: this.startingPosition.x, y: this.startingPosition.y}
        )

    }

    setDestionationPosition(destinationPosition) {

        this.destinationPosition = destinationPosition;

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

        // check if after redraw the token will be at the destination
        // if the token is at the destination then notify
        let wasAtDestination = true;

        ['x', 'y'].forEach(i => {

            if (this.position[i] !== this.destinationPosition[i]) {
                wasAtDestination = false;

                if (this.position[i] > this.destinationPosition[i]) {
                    this.position[i]--
                } else {
                    this.position[i]++
                }
            }
        })


        let allAtDestination = true;

        ['x', 'y'].forEach(i => {

            if (this.position[i] !== this.destinationPosition[i]) {
                allAtDestination = false;
                        
            }
        })

        if (!wasAtDestination && allAtDestination) {
        ludo.notify();
        }


        c.fillStyle = this.colour
        c.fill()
        c.closePath()
    }

}

export { Token }