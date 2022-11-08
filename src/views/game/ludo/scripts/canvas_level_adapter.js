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

        let oneByOne = true;

        if (oneByOne) {
            // t.move({jumpCount: jumpCount})

            // console.log(t.state)

            for (let i = t.state; i < t.state + jumpCount; i++) {
                // console.log(i)

                // console.log(this.level.player1State)

                if (i in this.level.player1State) {
                    let stateBoundaries = this.level.player1State[i]

                    // todo extract
                    let destinationPosition = {
                        x: stateBoundaries.column * Boundary.width + Boundary.width / 2,
                        y: stateBoundaries.row * Boundary.height + Boundary.height / 2
                    };

                    this.level.players[player].tokens[token].moveByOne({ destinationPosition: destinationPosition })

                } else {
                    console.log('integrity error: not in state object')
                }



            }

            t.state += jumpCount


            let stateBoundaries = this.level.player1State[t.state]
            // console.log('after', stateBoundaries)

            // todo extract
            let destinationPosition = {
                x: stateBoundaries.column * Boundary.width + Boundary.width / 2,
                y: stateBoundaries.row * Boundary.height + Boundary.height / 2
            }

            this.level.players[player].tokens[token].setDestionationPosition(destinationPosition)

            // t.state += jumpCount

            // let stateBoundaries = this.level.player1State[t.state]
            // console.log('after', stateBoundaries)

            // // todo extract
            // let destinationPosition = {
            //     x: stateBoundaries.column * Boundary.width + Boundary.width / 2,
            //     y: stateBoundaries.row * Boundary.height + Boundary.height / 2
            // }

            // this.level.players[player].tokens[token].setDestionationPosition(destinationPosition)



        } else {
            // t.move({jumpCount: jumpCount})

            // console.log(t.state)

            // let prevState = this.level.player1State[t.state];
            // console.log('prev', prevState)

            // for (let i = t.state; i < t.state + jumpCount; i++) {
            //     // const element ;
            //     console.log(i)

            // }

            // for (const [key, value] of Object.entries(this.level.player1State)) {
            //     console.log(key, value);
            // }


            t.state += jumpCount

            let stateBoundaries = this.level.player1State[t.state]
            // console.log('after', stateBoundaries)

            // todo extract
            let destinationPosition = {
                x: stateBoundaries.column * Boundary.width + Boundary.width / 2,
                y: stateBoundaries.row * Boundary.height + Boundary.height / 2
            }

            this.level.players[player].tokens[token].setDestionationPosition(destinationPosition)
        }



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