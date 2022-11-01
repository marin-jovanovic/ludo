import { Boundary } from "./boundary.js"


// todo stop on each tile for a sec,
// todo no diagonals

class CanvasLevelAdapter {

    constructor(canvasInstance, game) {
        this.canvas = canvasInstance;
        this.game = game;
        this.level = this.game.currentLevel;
    }

    startLevel = () => {

        this.animate(this.level, this.canvas);

    }

    movePosition({ player, token, jumpCount }) {

        let t = this.level.players[player].tokens[token];

        t.state += jumpCount

        let stateBoundaries = this.level.player1State[t.state]

        // todo extract
        let destinationPosition = {
            x: stateBoundaries.column * Boundary.width + Boundary.width / 2,
            y: stateBoundaries.row * Boundary.height + Boundary.height / 2
        }

        this.level.players[player].tokens[token].setDestionationPosition(destinationPosition)

    }

    moveTokenToStart({player, token}) {
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