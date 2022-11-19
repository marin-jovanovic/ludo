import {  CanvasStatic,CanvasReactive,  
    // Canvas
 } from "./canvas.js";
import { Level } from "./level.js";
import { ContentCreator } from "./content_creator.js";


class UserInterface {
    
    constructor(
        // canvasElement,
         s, r) {
        // this.canvas = new Canvas(canvasElement);

        this.staticCanvas = new CanvasStatic(s);

        this.reactiveCanvas = new CanvasReactive(r);

    }

}

class BusinessLogic extends ContentCreator {
    
    constructor(config) {
        super();
        this.currentLevel = new Level(config['map'], config['moves'], config['players']);
    }

    // startLevel = () => {
    //     this.notify({command: "animate", level: this.currentLevel});
    // }

}

class Game  {
    constructor(
        // canvasElement,
        
        s, r,
          config) {
        this.ui = new UserInterface(
            // canvasElement,
             s, r);

        this.bl = new BusinessLogic(config);

        // this.bl.currentLevel.subscribe({command: "animateOnce", s: this.ui.canvas.animateOnce});
        // this.bl.currentLevel.subscribe({command: "animateLoop", s: this.ui.canvas.animate});

        this.bl.currentLevel.subscribe({command: "animateOnce", s: this.ui.staticCanvas.animateOnce});
        this.bl.currentLevel.subscribe({command: "animateLoop", s: this.ui.reactiveCanvas.animate});


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
