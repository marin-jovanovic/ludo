import { BoardTile } from "./ui_board_tile.js"
import {getBoardTiles} from './layers.js'

class Canvas {
    
    constructor({element}) {
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
        super({element: element});

        
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

    constructor({element, playersToTokens}) {
        super({element: element});


        this.playersToTokens = playersToTokens;

        this.config = {
            // move token one by one
            // when one token stops moving another can start
            configOneByOne:  true,
            // wait for one token to reach destination (stops moving) before other token can be moved on board
            useBacklog: false,
        };


        // wait for one token to reach destination (stops moving) before other token can be moved on board
        // tokens scheduled for change

        this.backlog = [];

        
    
    }


    // moveToken = (notifArgs) => {
    //     /**
    //      * check if can move this token 
    //      * 
    //      * => 
    //      * if config.move one by one
    //      * then 
    //      * wait for other tokens to stop moving
    //      * 
    //      * else
    //      * move token
    //      * 
    //      * 
    //      */


    // }

    animate = (notifArgs) => {

        let level = notifArgs.level.levelState;
        console.log(level);
        // console.log(this.playersToTokens);

        let animateDriver = () => {

            this.canvas.animationId = requestAnimationFrame(animateDriver)

            this.clear()
            
            Object.values(this.playersToTokens).forEach(p => {

                Object.values(p.tokens).forEach(t => {

                    t.draw(this.context)

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