class Token {
    constructor({ position, colour, state }) {
        this.startingPosition = {x: position.x, y: position.y};
        this.position = position;
        
        // console.log(this.position)
        this.radius = 8

        // where is token on the board
        this.startingState = state
        this.state = state

        // console.log(this.state)
        this.colour = colour;

        this.destinationPosition = position;
    }

    restart() {
// console.log(this.state)
// console.log(this.startingState)
// console.log(this.position)
// console.log(this.startingPosition)

this.state = this.startingState;
this.destinationPosition = {x: this.startingPosition.x, y: this.startingPosition.y};

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

        ['x', 'y'].forEach(i => {
            if (this.position[i] !== this.destinationPosition[i]) {
                if (this.position[i] > this.destinationPosition[i]) {
                    this.position[i]--
                } else {
                    this.position[i]++
                }
            }
        })

        c.fillStyle = this.colour
        c.fill()
        c.closePath()
    }

}

export { Token }