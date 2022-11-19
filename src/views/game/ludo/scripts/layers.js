import { Token } from "./token.js";

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
let mappings = {
    q: 'green',
    w: 'blue',
    e: 'red',
    r: 'yellow',
};


function importAll(r) {
    return r.keys().map(r);
}

function getBoundaries({ map, Boundary }) {

    let images = importAll(require.context('/public/img/', false, /\.(png|jpe?g|svg)$/));

    let cloudImages = {};

    for (let i = 0; i < images.length; i++) {
        const cloudImage = new Image();
        cloudImage.src = images[i];

        let name = cloudImage.src.split("/img/")[1].split(".")[0]
        cloudImages[name] = cloudImage
    }



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
                        image: cloudImages[mapping[symbol].split(".")[0]]
                    
                    })
                )


            }

        })
    })

    return boundaries;
}



function remapPosition(i, j, Boundary) {
    return  {
        x: j * Boundary.width + Boundary.width / 2,
        y: i * Boundary.height + Boundary.height / 2
    }

}

function mapTokens({ map, Boundary, colour}) {

    let tokens = {};
    let c = 0;

    map.forEach((row, i) => {
        row.forEach((symbol, j) => {

            if (symbol in mappings && mappings[symbol] === colour) {

                let newToken = new Token({

                    position: remapPosition(i,j, Boundary),
                    colour: mappings[symbol],
                    state: -1,
                });

                // newToken.subscribe(subscriber);

                tokens[c] = newToken;
                c++;

            }

        })
    })

    return tokens;

}




export { 
    getBoundaries, 

    mapTokens
 }