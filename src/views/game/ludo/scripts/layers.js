/**
 * todo this needs to be rewriten with some backend api protocol which will send board and states
 * 
 */


import {
    remapTile
} from "./ui_comm.js";

function importAll(r) {
    return r.keys().map(r);
}

function getBoardTiles({
    map,
    Boundary
}) {
    /**
     * construct static content from api payload
     */

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

    let enumToImagePath = {};
    for (let i = 0; i < importedImages.length; i++) {

        let name = importedImages[i].split("/img/")[1].split(".")[0];

        enumToImagePath[name] = importedImages[i]
    }

    let boardTiles = [];

    map.forEach((row, i) => {
        row.forEach((symbol, j) => {

            if (symbol in mapping) {

                let image = new Image();
                image.src = enumToImagePath[mapping[symbol].split(".")[0]];

                boardTiles.push(
                    new Boundary({
                        position: remapTile({
                            x: j,
                            y: i,
                            Boundary: Boundary
                        }),

                        image: image

                    })
                )

            }

        })
    })

    return boardTiles;
}






export {
    getBoardTiles,
    // mapTokens
}