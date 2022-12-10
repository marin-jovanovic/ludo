import { BoardTile } from "./ui_board_tile.js"
import {getBoardTiles} from './layers.js'

class Canvas {
    
    constructor(element) {
        this.canvas = element;

        // this.canvas.width = 600;
        // this.canvas.height = 600;
        this.canvas.width = innerWidth;
        this.canvas.height = innerHeight;

        this.context = this.canvas.getContext("2d");
        this.animationId;
  
    }

    clear = () => {

        // leave no trace
        this.context.clearRect(0, 0, this.canvas.width, this.canvas.height)

    }

}

class CanvasStatic extends Canvas {
    constructor({element, map}) {
        super(element);
    
        this.boardTiles = getBoardTiles({ 
            map: map, 
            Boundary: BoardTile 
        })
    }

    animateOnce = () => {

        // board
        this.boardTiles.forEach((b) => {
             b.draw(this.context)
        })
   
    }
}

class CanvasReactive extends Canvas {

    constructor(element) {
        super(element);

        // init token state

        // tokens scheduled for change

        // wait for one token to reach destination (stops moving) before other token can be moved on board
        this.backlog = [];
        this.useBacklog = false;

    }


    moveToken = (notifArgs) => {
        /**
         * check if can move this token 
         * 
         * => 
         * if config.move one by one
         * then 
         * wait for other tokens to stop moving
         * 
         * else
         * move token
         * 
         * 
         */


        console.log(notifArgs)

        // this.__movePositionDriver({
        // player: notifArgs.player,
        // token: notifArgs.token,
        // jumpCount: notifArgs.jumpCount,
        // });

        // if (this.useBacklog) {
        //     if (this.backlog.length === 0) {
        //       this.__movePositionDriver({
        //         player: player,
        //         token: token,
        //         jumpCount: jumpCount,
        //       });
        //     }
    
        //     this.backlog.push([player, token, jumpCount]);
        
        // } else {
        //     this.__movePositionDriver({
        //       player: player,
        //       token: token,
        //       jumpCount: jumpCount,
        //     });
        // }

    }

    animate = (notifArgs) => {

        let level = notifArgs.level.levelState;

        // let animateDriver = () => {

        //     this.clear();

        //     Object.values(level.players).forEach(p => {

        //         Object.values(p.tokens).forEach(t => {

        //             t.draw(this.context)

        //         });
        
        //     });

        // }

        // animateDriver();

        let canvas = this.canvas;
        let context = this.context;

        // function animateDriver() {
        let animateDriver = () => {

            // setup
            canvas.animationId = requestAnimationFrame(animateDriver)
            // canvas.clear();

                    // leave no trace
            context.clearRect(0, 0, this.canvas.width, this.canvas.height)
            
                // canvas.clear();

                Object.values(level.players).forEach(p => {

                    Object.values(p.tokens).forEach(t => {

                        t.draw(context)

                    });
            
                });

        
        }
        
        animateDriver();

    }

  

}


export { 
    CanvasStatic,
    CanvasReactive
}