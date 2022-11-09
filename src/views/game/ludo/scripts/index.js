import { CanvasGame } from "./canvas.js";
import { CanvasLevelAdapter } from "./canvas_level_adapter.js";
import { Level } from "./level.js";

class Game {
    constructor() {

        this.levelInstance;
        this.canvasInstance;
        this.gameInstance;
        this.canvasLevelAdapter;

        this.canvasInstance = new CanvasGame();
    }

    setConfig(config) {

        this.levelInstance = new Level(config['map'], config['moves']);
        this.currentLevel = this.levelInstance;

        this.canvasLevelAdapter = new CanvasLevelAdapter(
            this.canvasInstance,
            this.currentLevel
        );

        this.canvasLevelAdapter.startLevel();
    }

    movePosition({ player, token, jumpCount }) {

        this.canvasLevelAdapter.movePosition({ player: player, token: token, jumpCount: jumpCount });

    }

    restartToken({ player, token }) {
        this.canvasLevelAdapter.moveTokenToStart({ player: player, token: token });
    }


}

// function addEventListenerToDocument(type, listener) {
//     addEventListener(type, listener)
// }

// function removeEventListenerToDocument(type, listener) {
//     removeEventListener(type, listener)
// }

let game;
// 
// let game = new Game();


window.addEventListener('load', () => {
    console.log('load')
    game = new Game();
});


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
    game,

    subscribe,
    unsubscribe,
    notify,


}
