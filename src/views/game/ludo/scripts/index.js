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

        this.isConfigSet = false;

        this.subscribers = new Set();

    }


    subscribe(s) {
        this.subscribers.add(s);
    }

    unsubscribe(s) {
        this.subscribers.delete(s);
    }

    notify() {

        this.subscribers.forEach((i) => {
            // console.log('notify')
            i();
        });
    }


    setConfig(config) {
        this.isConfigSet = true;

        this.levelInstance = new Level(config['map'], config['moves'], config['players']);
        this.currentLevel = this.levelInstance;

        this.canvasLevelAdapter = new CanvasLevelAdapter(
            this.canvasInstance,
            this.currentLevel
        );

        this.canvasLevelAdapter.startLevel();
    }

    movePosition({ player, token, jumpCount }) {
        if (!this.isConfigSet) {
            console.log('integrity error')
        } else {
            this.canvasLevelAdapter.movePosition({ player: player, token: token, jumpCount: jumpCount });
        }
    }

    restartToken({ player, token }) {
        if (!this.isConfigSet) {
            console.log('integrity error')
        } else {
            this.canvasLevelAdapter.moveTokenToStart({ player: player, token: token });
        }
    }


}

let game;

window.addEventListener('load', () => {
    game = new Game();
});

function getGame() {
    if (game) {
        return game
    } else {
        console.log('integrity error')
    }
}


export const ludo = {
    getGame,
}
