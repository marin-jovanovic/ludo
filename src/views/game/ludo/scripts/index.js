import { CanvasGame } from "./canvas.js";
import { CanvasLevelAdapter } from "./canvas_level_adapter.js";
import { Level } from "./level.js";
import { Game } from "./game.js";


let levelInstance;
let canvasInstance;
let gameInstance;

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

    let canvasLevelAdapter = new CanvasLevelAdapter(
        canvasInstance,
        gameInstance
    );

    canvasLevelAdapter.startLevel();

}


// export { addEventListenerToDocument, removeEventListenerToDocument };


export const ludo = {
    startup,
    }
    