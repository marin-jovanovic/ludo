import { CanvasGame } from "./canvas.js";
import { CanvasLevelAdapter } from "./canvas_level_adapter.js";
import { Level } from "./level.js";
import { Game } from "./game.js";


let levelInstance;
let canvasInstance;
let gameInstance;
let canvasLevelAdapter;
// function addEventListenerToDocument(type, listener) {
//     addEventListener(type, listener)
// }

// function removeEventListenerToDocument(type, listener) {
//     removeEventListener(type, listener)
// }

window.onload = function () {
    startup();

}

function startup() {
    canvasInstance = new CanvasGame();
    levelInstance = new Level();
    gameInstance = new Game(levelInstance);

    canvasLevelAdapter = new CanvasLevelAdapter(
        canvasInstance,
        gameInstance
    );

    canvasLevelAdapter.startLevel();

}

function    movePosition({player, token, jumpCount}) {

            canvasLevelAdapter.movePosition({ player: player, token: token, jumpCount: jumpCount });
}


// class GameDriver {
//     constructor() {
//         this.canvasInstance = new CanvasGame();
//         this.levelInstance = new Level();
//         this.gameInstance = new Game(this.levelInstance);
    
//         this.canvasLevelAdapter = new CanvasLevelAdapter(
//             this.canvasInstance,
//             this.gameInstance
//         );
    
//         this.canvasLevelAdapter.startLevel();
    
            

//     }


//     movePosition({player, token, jumpCount}) {
//         this.canvasLevelAdapter.movePosition({ player: player, token: token, jumpCount: jumpCount })

//     }





// }

// let gameDriver = new GameDriver();


// export {Game}

// class Game

// function getCanvasLevel

// export { addEventListenerToDocument, removeEventListenerToDocument };


export const ludo = {
    startup,
    movePosition
    // gameDriver
    }
    