import { Canvas } from "./canvas.js";
import { CanvasLevelAdapter } from "./canvas_level_adapter.js";
import { Level } from "./level.js";

class ContentCreator {

    constructor() {
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
            i();
        });
    }

}

class UserInterface {
    constructor(canvasElement) {
        this.canvas = new Canvas(canvasElement);
    }

    onNotification() {
        console.log("on notif")
    }
}

class BusinessLogic extends ContentCreator {
    constructor(config) {
        super();
        this.level = new Level(config['map'], config['moves'], config['players']);
    }
}

class Game  {
    constructor(canvasElement, config) {

        let ui = new UserInterface(canvasElement);

        let bl = new BusinessLogic(config);

        bl.subscribe(ui.onNotification);

        this.canvasLevelAdapter = new CanvasLevelAdapter(
            ui.canvas,
            bl.level,
            config
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

export const ludo = {
    Game,
}
