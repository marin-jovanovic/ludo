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

function movePosition({player, token, jumpCount}) {

    canvasLevelAdapter.movePosition({ player: player, token: token, jumpCount: jumpCount });

    // notify();

}

function restartToken({player, token}) {
    canvasLevelAdapter.moveTokenToStart({player: player, token: token});


}

let subscribers = new Set();

function subscribe(s) {
    subscribers.add(s);
}

function unsubscribe(s) {
subscribers.delete(s);
}

function notify() {

    subscribers.forEach((i) => {
        i();
    });
}

export const ludo = {
    startup,
    movePosition,
    restartToken,

    subscribe,
    unsubscribe,
    notify,


}
    