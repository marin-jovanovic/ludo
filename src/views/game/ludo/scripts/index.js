import {  CanvasStatic,CanvasReactive } from "./ui_canvas.js";
import { Level } from "./bl_level.js";

import { mapTokens } from "./layers.js";
import { BoardTile } from "./ui_board_tile.js";

class UserInterface {
    
    constructor({
        staticCanvasElement, 
        reactiveCanvasElement,
        map,
        playersToTokens
    }) {


        this.staticCanvas = new CanvasStatic({
            element: staticCanvasElement,
            map: map 
        });


        this.reactiveCanvas = new CanvasReactive({
            element:reactiveCanvasElement,
            playersToTokens: playersToTokens,
        });

    }

}

class BusinessLogic {
    
    constructor({config, tokens}) {
        this.currentLevel = new Level({
            moves: config['moves'], 
            players: config['players'],
            tokens: tokens,
        });
    }

}

class Game {
    constructor(staticCanvasElement, reactiveCanvasElement, config) {

        let uiPart = {};
        let blPart = {};

        for (const [playerId, playerMetadata] of Object.entries(config['players'])) {

            let r = mapTokens({
                map: config['map'],
                Boundary: BoardTile,
                colour: playerMetadata.colour,
            });

            blPart[playerId] = {
                username: playerMetadata.username,
                tokens: r[0]
            }

            uiPart[playerId] = {
                username: playerMetadata.username,
                tokens: r[1]
            }

        }

        this.ui = new UserInterface({
            staticCanvasElement: staticCanvasElement, 
            reactiveCanvasElement: reactiveCanvasElement,
            map: config['map'],
            playersToTokens: uiPart,
        });

        this.bl = new BusinessLogic({config:config, tokens: blPart});

        this.bl.currentLevel.subscribe({
            command: "drawBoard", 
            s: this.ui.staticCanvas.animateOnce
        });
        
        this.bl.currentLevel.subscribe({
            command: "animateTokens", 
            s: this.ui.reactiveCanvas.animate
        });

        for (const playerComposite of Object.values(this.ui.reactiveCanvas.playersToTokens)) {

            for (const t of Object.values(playerComposite.tokens)) {
                t.subscribe({
                    command: "UiUpdated",
                    s: this.bl.currentLevel.updated
                });
            }

        }
  

        this.bl.currentLevel.start();

    }

    movePosition({ playerId, tokenId, jumpCount }) {
        /**
         * @player wants to move @token for @jumpCount positions
         * 
         * this can @player only call when it can not be determinated automatically which token should be moved
         * 
         * this is the case when there are multiple tokens on the board, or @player rolled 6 and can get one token out of the starting pool or move another @token on the board for 6 positions
         * 
         */


        this.bl.currentLevel.movePosition({
            playerId: playerId, 
            tokenId: tokenId, 
            jumpCount: jumpCount
        });
        
    }

    restartToken({ playerId, tokenId }) {
        /**
         * @player wants to move @token to starting position
         * this is not something that user can do
         * 
         * this can only be done programaticaly => user does not have the option to chose this
         * 
         */


        this.bl.currentLevel.restartToken({ 
            playerId:playerId, 
            tokenId:tokenId
        }); 

    }

}

export const ludo = {
    Game,
}
