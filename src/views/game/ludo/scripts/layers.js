import { Token } from "./token.js";

import { createImage } from "./image.js";



function importAll(r) {
    return r.keys().map(r);
}

function getBoardTiles({ map, Boundary }) {

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


    // todo render off screen images

    let importedImages = importAll(
        require.context('/public/img/', false, /\.(png|jpe?g|svg)$/)
    );

    let images = {};

    for (let i = 0; i < importedImages.length; i++) {

        let image = createImage({
            source: importedImages[i]
        });

        let name = image.src.split("/img/")[1].split(".")[0];

        images[name] = image
    }

    let boardTiles = [];

    map.forEach((row, i) => {
        row.forEach((symbol, j) => {

            if (symbol in mapping) {

                boardTiles.push(
                    new Boundary({
                        position: {
                            x: Boundary.width * j,
                            y: Boundary.height * i
                        },
                        image: images[mapping[symbol].split(".")[0]]
                    
                    })
                )

            }

        })
    })

    return boardTiles;
}



function remapPosition(i, j, Boundary) {
    return  {
        x: j * Boundary.width + Boundary.width / 2,
        y: i * Boundary.height + Boundary.height / 2
    }

}

function mapTokens({ map, Boundary, colour}) {

    let mappings = {
        q: 'green',
        w: 'blue',
        e: 'red',
        r: 'yellow',
    };
    
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
    getBoardTiles, 

    mapTokens,
    remapPosition
 }