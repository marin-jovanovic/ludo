import { Boundary } from "./boundary.js"

class CanvasLevelAdapter {

    constructor(canvasInstance, game) {
        this.canvas = canvasInstance;
        this.game = game;
        this.level = this.game.currentLevel;

        this.configOneByOne = true;

    }

    startLevel = () => {

        this.animate(this.level, this.canvas);

    }

    _tileToCoordinates(stateBoundaries) {
        // tile (x,y) to coordinate (pixels x,y ?) 
        // find center of that pixels posiiton return it

        // todo extract
        return {
            x: stateBoundaries.column * Boundary.width + Boundary.width / 2,
            y: stateBoundaries.row * Boundary.height + Boundary.height / 2
        };

    }

    movePosition({ player, token, jumpCount }) {

        let t = this.level.players[player].tokens[token];

        if (this.configOneByOne) {

            for (let i = t.state; i < t.state + jumpCount; i++) {

                if (i in this.level.player1State) {
                    let stateBoundaries = this.level.player1State[i]

                    let destinationPosition = this._tileToCoordinates(stateBoundaries);

                    this.level.players[player].tokens[token].moveByOne({ destinationPosition: destinationPosition })

                } else {
                    console.log('integrity error: not in state object')
                }

            }

        }

        t.state += jumpCount

        let stateBoundaries = this.level.player1State[t.state]

        let destinationPosition = this._tileToCoordinates(stateBoundaries);

        this.level.players[player].tokens[token].setDestionationPosition(destinationPosition)

    }

    moveTokenToStart({ player, token }) {
        this.level.players[player].tokens[token].restart();
    }

    animate(level, canvas) {



        function animateDriver() {

            // setup
            canvas.animationId = requestAnimationFrame(animateDriver)

            canvas.clear();


            // board
            level.boundaries.forEach((b) => {
                b.draw(canvas.context)
            })

            // tokens

            for (const p of Object.values(level.players)) {

                for (const t of Object.values(p.tokens)) {
                    t.draw(canvas.context)
                }

            }


        }

        animateDriver();

    }
}



export { CanvasLevelAdapter }