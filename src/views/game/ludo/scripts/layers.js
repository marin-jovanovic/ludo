import { Token } from "./token.js";

// import { createImage } from "./ui_image.js";



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
                        position: {
                            x: Boundary.width * j,
                            y: Boundary.height * i
                        },
                        image: image
                
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

// function getDictionary({}) {
//     return {
//         "a": {"type": "token", "id": "1"},
//         "b": {"type": "token"},
//         "c": {"type": "token"},
//         "d": {"type": "token"}
//     }
// }


function mapTokens({ map, Boundary, colour}) {

    // console.log(map)
    // console.log(Boundary)

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

                tokens[c] = newToken;
                c++;

            }

        })
    })

    // console.log(tokens)

    return tokens;

}




export { 
    getBoardTiles, 
    mapTokens,
    remapPosition
}