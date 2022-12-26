import {
    BoardTile
} from "./ui_board_tile.js"
import {
    getBoardTiles
} from './layers.js'

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

class CanvasReactive extends Canvas {

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

                    t.draw(this.context)

                });

            });


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


        // xy -> {playerId, tokenId}


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

        console.log(x)

        for (const [xCoordinate, yCoordinateToTokens] of Object.entries(x)) {
            // console.log(xCoordinate, yCoordinateToTokens)

            for (const [yCoordinate, tokens] of Object.entries(yCoordinateToTokens)) {
                console.log(xCoordinate, yCoordinate, tokens)

                let tokensOnSameSpot = tokens.length;
                console.log(tokensOnSameSpot)


                tokens.forEach(i => {
                    i.token.number = {
                        c: tokensOnSameSpot
                    };
                })

                // tokens.token.number = tokensOnSameSpot;


            }


        }


    }



}


export {
    CanvasStatic,
    CanvasReactive
}