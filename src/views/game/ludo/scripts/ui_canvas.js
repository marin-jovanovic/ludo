import {
    BoardTile
} from "./ui_board_tile.js"
import {
    getBoardTiles
} from './layers.js'
import {
    circleCollidesWithPoint
} from "./collisions.js";
import {
    ContentCreator
} from "./content_creator.js";

class Canvas {

    constructor({
        element
    }) {
        this.canvas = element;

        // this.canvas.width = 600;
        // this.canvas.height = 600;
        this.canvas.width = innerWidth;
        this.canvas.height = innerHeight;

        this.context = this.canvas.getContext("2d");
        this.animationId;

    }

    clear = () => {

        // leave no trace
        this.context.clearRect(0, 0, this.canvas.width, this.canvas.height)

    }

}

class DeliverableCanvas extends ContentCreator {

    constructor({
        element
    }) {
        super();

        this.canvas = element;

        // this.canvas.width = 600;
        // this.canvas.height = 600;
        this.canvas.width = innerWidth;
        this.canvas.height = innerHeight;

        this.context = this.canvas.getContext("2d");
        this.animationId;

    }

    clear = () => {

        // leave no trace
        this.context.clearRect(0, 0, this.canvas.width, this.canvas.height)

    }


}


class CanvasStatic extends Canvas {
    constructor({
        element,
        map
    }) {
        super({
            element: element
        });


        this.boardTiles = getBoardTiles({
            map: map,
            Boundary: BoardTile
        })
    }

    animateOnce = () => {

        // board
        this.boardTiles.forEach((b) => {
            b.draw(this.context)
        })

    }
}

class CanvasReactive extends DeliverableCanvas {

    constructor({
        element,
        playersToTokens
    }) {
        super({
            element: element
        });


        this.playersToTokens = playersToTokens;

        this.config = {
            // move token one by one
            // when one token stops moving another can start
            configOneByOne: true,
            // wait for one token to reach destination (stops moving) before other token can be moved on board
            useBacklog: false,
        };

        this.mousePosition = {
            x: 0,
            y: 0
        }

        //         this.canvas.addEventListener("click", (e) => {
        // console.log(e)
        //         })

        // what if multiple on same

        // mousemove
        this.canvas.addEventListener('click', (event) => {


            this.mousePosition.x = event.layerX;
            this.mousePosition.y = event.layerY;

            // console.log(this.playersToTokens)

            Object.values(this.playersToTokens).forEach(p => {

                for (const [id, t] of Object.entries(p.tokens)) {

                    if (circleCollidesWithPoint({
                            circle: t,
                            point: this.mousePosition
                        })) {

                        t.collides = true;

                        // console.log("clicked", t.position)

                        new Promise((r) => setTimeout(r, 500)).then(() => {
                            t.collides = false
                        });

                        console.log(p.username, id)

                        this.notify({
                            command: "tokenSelected",
                            username: p.username,
                            tokenId: id
                        });


                    } else {
                        // unset all others
                        t.collides = false;
                    }



                }


                // Object.values(p.tokens).forEach(t => {


                //     // if (t.position.x === 100 && t.position.y === 460) {
                //         // console.log(t.position, t.radius, this.mousePosition);

                //         if (circleCollidesWithPoint({circle: t, point: this.mousePosition})) {

                //             t.collides =  true;

                //             console.log("clicked", t.position)

                //              new Promise((r) => setTimeout(r, 500)).then(() => {
                //                 t.collides = false
                //             });

                //             console.log(p.username, p, t)


                //         } else {
                //             // unset all others
                //             t.collides =  false;
                //         }


                // });
            });

        });


        // wait for one token to reach destination (stops moving) before other token can be moved on board
        // tokens scheduled for change

        // this.backlog = [];



    }

    animate = () => {





        let animateDriver = () => {

            this.canvas.animationId = requestAnimationFrame(animateDriver)

            this.clear()

            Object.values(this.playersToTokens).forEach(p => {

                Object.values(p.tokens).forEach(t => {


                    t.draw(this.context, this.mousePosition);

                    // this.context.fillStyle = 'red';

                });

            });


            // this is cardinality part

            let x = {}

            for (const [playerId, playerMeta] of Object.entries(this.playersToTokens)) {

                for (const [tokenId, tokenMeta] of Object.entries(playerMeta.tokens)) {

                    let t = {
                        playerId: playerId,
                        tokenId: tokenId,
                        token: tokenMeta
                    }


                    if (tokenMeta.position.x in x) {

                        if (tokenMeta.position.y in x[tokenMeta.position.x]) {
                            x[tokenMeta.position.x][tokenMeta.position.y].push(t)

                        } else {
                            x[tokenMeta.position.x][tokenMeta.position.y] = [t]

                        }


                    } else {


                        x[tokenMeta.position.x] = {}
                        x[tokenMeta.position.x][tokenMeta.position.y] = [t]


                    }


                }

            }


            // todo: enhancment: when they stop coliding then rewrite numbers as 1 and 1, not 2


            for (const yCoordinateToTokens of Object.values(x)) {

                for (const tokens of Object.values(yCoordinateToTokens)) {

                    let tokensOnSameSpot = tokens.length;

                    tokens.forEach(i => {
                        i.token.number = {
                            c: tokensOnSameSpot
                        };
                    })

                    // tokens.token.number = tokensOnSameSpot;


                }


            }

        }

        animateDriver();




    }



}


export {
    CanvasStatic,
    CanvasReactive
}