// import { Pellet } from "./pellet.js"
// import { PowerUp } from "./powerup.js"
import { createImage } from "./image.js"
import { Token } from "./token.js"
const mapping = {
    "-": "pipeHorizontal.png",
    "|": "pipeVertical.png",
    "1": "pipeCorner1.png",
    "2": "pipeCorner2.png",
    "3": "pipeCorner3.png",
    "4": "pipeCorner4.png",
    "b": "block.png",
    "[": "capLeft.png",
    "]": "capRight.png",
    "_": "capBottom.png",
    "^": "capTop.png",
    "+": "pipeCross.png",
    "5": "pipeConnectorTop.png",
    "6": "pipeConnectorRight.png",
    "7": "pipeConnectorBottom.png",
    "8": "pipeConnectorLeft.png"
}

const pathPrefix = "./img/"



function getBoundaries({ map, Boundary }) {
    let boundaries = [];

    map.forEach((row, i) => {
        row.forEach((symbol, j) => {

            if (symbol in mapping) {

                boundaries.push(
                    new Boundary({
                        position: {
                            x: Boundary.width * j,
                            y: Boundary.height * i
                        },
                        image: createImage(pathPrefix + mapping[symbol])
                    })
                )

            }

        })
    })

    return boundaries;
}


let mappings = {
    q: 'green',
    w: 'blue',
    e: 'red',
    r: 'yellow',
}

function mapTokens({ map, Boundary, colour }) {


    let tokens = {};
    let c = 0;

    map.forEach((row, i) => {
        row.forEach((symbol, j) => {

            if (symbol in mappings && mappings[symbol] === colour) {

                let newToken = new Token({
                  
                    position: {
                        x: j * Boundary.width + Boundary.width / 2,
                        y: i * Boundary.height + Boundary.height / 2
                    },
                    colour: mappings[symbol],
                    state: -1
                });

                tokens[c] = newToken;
                c++;

            }

        })
    })

    return tokens;

}

function getTokens({ map, Boundary }) {

    let tokens = {};

    map.forEach((row, i) => {
        row.forEach((symbol, j) => {

            if (symbol in mappings) {

                let newToken = new Token({
                    position: {
                        x: j * Boundary.width + Boundary.width / 2,
                        y: i * Boundary.height + Boundary.height / 2
                    },
                    colour: mappings[symbol],
                    state: 'start'
                });

                if (mappings[symbol] in tokens) {
                    tokens[mappings[symbol]].push(newToken);
                } else {
                    tokens[mappings[symbol]] = [newToken];
                }

            }

        })
    })

    return tokens;

}


export { 
    getBoundaries, 

    getTokens, 
    mapTokens
 }