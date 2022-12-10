import {  CanvasStatic,CanvasReactive } from "./ui_canvas.js";
import { Level } from "./bl_level.js";


class UserInterface {
    
    constructor({
        staticCanvasElement, 
        reactiveCanvasElement,
        map
    }) {

        this.staticCanvas = new CanvasStatic({
            element: staticCanvasElement,
            map: map 
        });

        this.reactiveCanvas = new CanvasReactive(reactiveCanvasElement);

    }

}

class BusinessLogic {
    
    constructor(config) {
        this.currentLevel = new Level(
            config['map'], 
            config['moves'], 
            config['players']
        );
    }

}

class Game {
    constructor(staticCanvasElement, reactiveCanvasElement, config) {

        this.ui = new UserInterface({
            staticCanvasElement: staticCanvasElement, 
            reactiveCanvasElement: reactiveCanvasElement,
            map: config['map']
        });

        this.bl = new BusinessLogic(config);

        this.bl.currentLevel.subscribe({
            command: "drawBoard", 
            s: this.ui.staticCanvas.animateOnce
        });
        
        this.bl.currentLevel.subscribe({
            command: "animateTokens", 
            s: this.ui.reactiveCanvas.animate
        });

        this.bl.currentLevel.subscribe({
            command: "tokenMoved", 
            s: this.ui.reactiveCanvas.moveToken
        });

        this.bl.currentLevel.start();

    }

    movePosition({ player, token, jumpCount }) {
        /**
         * @player wants to move @token for @jumpCount positions
         * 
         * this can @player only call when it can not be determinated automatically which token should be moved
         * 
         * this is the case when there are multiple tokens on the board, or @player rolled 6 and can get one token out of the starting pool or move another @token on the board for 6 positions
         * 
         */


        this.bl.currentLevel.movePosition({player: player, token: token, jumpCount: jumpCount})
        
    }

    restartToken({ player, token }) {
        /**
         * @player wants to move @token to starting position
         * this is not something that user can do
         * 
         * this can only be done programaticaly => user does not have the option to chose this
         * 
         */


        this.bl.currentLevel.restartToken({ player:player, token:token }) 

    }

}

export const ludo = {
    Game,
}
