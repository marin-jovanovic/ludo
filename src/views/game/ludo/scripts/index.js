import { Canvas } from "./canvas.js";
import { Level } from "./level.js";
import { Boundary } from "./boundary.js";


class ContentCreator {

    constructor() {
        this.subscribers = {};
    }

    subscribe({command, s}) {

        if (command in this.subscribers) {

            this.subscribers[command].add(s);

        } else {
            this.subscribers[command] = new Set();
            this.subscribers[command].add(s);
        }

    }

    unsubscribe({command, s}) {
        this.subscribers[command].delete(s);
    }

    notify({command, ...args}) {

        this.subscribers[command].forEach((i) => {
            i(args);
        });
    }

}

class UserInterface {
    constructor(canvasElement) {
        this.canvas = new Canvas(canvasElement);

        this.animate = this.animate.bind(this);

    }

    animate(notifArgs) {

        let level = notifArgs.level;
        let canvas  = this.canvas;

        function animateDriver() {

            // setup
            canvas.animationId = requestAnimationFrame(animateDriver)

            canvas.clear();

            // board
            level.boundaries.forEach((b) => {
                b.draw(canvas.context)
            })

            // tokens

            for (const p of Object.values(level.players)) {

                for (const t of Object.values(p.tokens)) {
                    t.draw(canvas.context)
                }

            }


        }

        animateDriver();

    }


}

class BusinessLogic extends ContentCreator {
    constructor(config) {
        super();
        this.level = new Level(config['map'], config['moves'], config['players']);
    }

    startLevel = () => {
        this.notify({command: "animate", level: this.level});
    }

}

class Game  {
    constructor(canvasElement, config) {

        this.ui = new UserInterface(canvasElement);

        this.bl = new BusinessLogic(config);

        this.bl.subscribe({command: "animate", s: this.ui.animate});

        // this.canvas = this.ui.canvas;
        this.level = this.bl.level;
        
        this.notify = this.notify.bind(this);



        // todo what is this used for?
        this.configOneByOne = true;

        // wait for one token to reach destination (stops moving) before other token can be moved on board
        this.backlog = [];
        this.useBacklog = false;

        this.bl.startLevel();

    }

    movePosition({ player, token, jumpCount }) {

    
            if (this.useBacklog) {
                if (this.backlog.length === 0) {
                  this.__movePositionDriver({
                    player: player,
                    token: token,
                    jumpCount: jumpCount,
                  });
                }
        
                this.backlog.push([player, token, jumpCount]);
              } else {
                this.__movePositionDriver({
                  player: player,
                  token: token,
                  jumpCount: jumpCount,
                });
              }
        
    }

    restartToken({ player, token }) {
        this.moveTokenToStart({ player: player, token: token });
    }

    notify() {
        this.backlog.shift();
  
        if (this.backlog.length === 0) {
          return;
        }
  
        let first = this.backlog[0];
  
        // todo fix, add param for action, or multiple queues
        if (first.length === 2) {
          this.moveTokenToStart({ player: first[0], token: first[1] });
        } else {
          this.movePosition({
            player: first[0],
            token: first[1],
            jumpCount: first[2],
          });
        }
      }



    _tileToCoordinates(stateBoundaries) {
        // tile (x,y) to coordinate (pixels x,y ?) 
        // find center of that pixels posiiton return it

        // todo extract
        return {
            x: stateBoundaries.column * Boundary.width + Boundary.width / 2,
            y: stateBoundaries.row * Boundary.height + Boundary.height / 2
        };

    }


    __movePositionDriver({ player, token, jumpCount }) {
        let t = this.level.players[player].tokens[token];

        if (this.configOneByOne) {

            for (let i = t.state; i < t.state + jumpCount; i++) {

                if (i in this.level.player1State) {
                    let stateBoundaries = this.level.player1State[i]

                    let destinationPosition = this._tileToCoordinates(stateBoundaries);

                    this.level.players[player].tokens[token].moveByOne({ destinationPosition: destinationPosition })

                } else {
                    console.log('integrity error: not in state object')
                }

            }

        }

        t.state += jumpCount

        let stateBoundaries = this.level.player1State[t.state]

        let destinationPosition = this._tileToCoordinates(stateBoundaries);

        this.level.players[player].tokens[token].setDestionationPosition(destinationPosition)

    }



    __restartToken({ player, token }) {
        this.level.players[player].tokens[token].restart();

    }

    moveTokenToStart({ player, token }) {

        if (this.useBacklog) {
            if (this.backlog.length === 0) {
              this.__restartToken({ player: player, token: token });
            }
    
            this.backlog.push([player, token]);
        } else {
            this.__restartToken({ player: player, token: token });
        }

    }

   
}

export const ludo = {
    Game,
}
