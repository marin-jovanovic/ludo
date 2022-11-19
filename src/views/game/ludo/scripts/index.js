import {  CanvasStatic,CanvasReactive } from "./canvas.js";
import { Level } from "./level.js";


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

        this.bl.currentLevel.subscribe({command: "drawBoard", s: this.ui.staticCanvas.animateOnce});
        this.bl.currentLevel.subscribe({command: "animateTokens", s: this.ui.reactiveCanvas.animate});

        this.bl.currentLevel.start();

    }

    movePosition({ player, token, jumpCount }) {
    
        this.bl.currentLevel.movePosition({player: player, token: token, jumpCount: jumpCount})
        
    }

    restartToken({ player, token }) {

        this.bl.currentLevel.restartToken({ player:player, token:token }) 

    }

}

export const ludo = {
    Game,
}
