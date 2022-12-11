import { remapPosition } from "./ui_comm.js";
import { BoardTile } from "./ui_board_tile.js";
import { ContentCreator } from "./content_creator.js";
import {getConfig} from "./token.js";

class Level extends ContentCreator {
    constructor({ moves, players, tokens}) {
        super();

        this.config = {
            // move token one by one
            // when one token stops moving another can start
            configOneByOne:  true,
            // wait for one token to reach destination (stops moving) before other token can be moved on board
            useBacklog: false,
        };

  
        // wait for one token to reach destination (stops moving) before other token can be moved on board
        this.backlog = [];

        //1 todo extract colour to config
        //2 sta kad se preklope / pojedu
        //3 sta kad se preklope useri, (two users at same tile)
        
        // DTO - data transfer object
        this.levelState = this.fetchLevelState({players: players, moves: moves, tokens: tokens});
    
    }

    start() {
        /**
         * start level, notify all listeners
         */

        this.notify({
            command: "drawBoard"
        });

        this.notify({
            command: "animateTokens", 
            level: this, 
        });

    }

    // todo rewrite
    fetchLevelState({players,  moves, tokens}) {
        /**
         * return board state
         * 
         */


        let p = {};
        let c = 0; 
      
        for (const playerId of Object.keys(players)) {

            p[playerId] = {
                ...tokens[playerId],
                state: moves[c]
            }

              c += 1;

        }



        let levelState = {

            // basic game metadata
            status: {
                isGameDone: false,
                quit: ['1'],
                won: []
            },
            // for each player info
            players: p
        }
        

        return levelState;

    }

    movePosition({ player, token, jumpCount }) {
        /**
            check are performed in backend? 

        * can be called by user or automatic (game replay)
         * 
         * perform check if can be done
         * 
         * move @player @token for @jumpCount positions
         * 
         * notify that level is updated
         * 
         * 
         */




        let isLegalMove =  this.__movePositionDriver({
            player: player,
            token: token,
            jumpCount: jumpCount,
          });

        if (isLegalMove) {


            // move token on bl
            
            // notify to move token on ui

            console.log("todo notify")
            // this.notify({
            //     command: "tokenMoved", 
            //     player: player,
            //     token: token,
            //     jumpCount: jumpCount,
                    
            //     // level: this, 
            // });
        }
   
    }

    restartToken({ player, token }) {
        this.levelState.players[player].tokens[token].restart();
    }

    getObjectMaxKey(obj) {
        return Object.keys(obj).reduce((a, b) => obj[a] > obj[b] ? a : b);
    }

    __movePositionDriver({ player, token, jumpCount }) {

        if (!(player in this.levelState.players)) {
            console.log("err: unknown player", player);
            return;
        }

        if (!(token in this.levelState.players[player].tokens)) {
            console.log("err: unknown token", token);
            return;
        }

        // if (jumpCount === 0) {
        //     console.log("no movement");
        //     return;
        // }

        // current token 
        let t = this.levelState.players[player].tokens[token];

        switch (t.pool) {
            case getConfig()["pool"]["start"]:
                t.pool = getConfig()["pool"]["live"];
                t.state = 0;
                break;
            
            case getConfig()["pool"]["live"]:

                // check if can move so much 

                console.log(
                    t.state,
                    jumpCount,
                    this.levelState.players[player].state
                )

                if (
                    t.state + jumpCount
                    in this.levelState.players[player].state
                ) {

                    console.log("can jump");

                                    // bl
                    t.move({
                        count: jumpCount, 
                    });

                } else {
                    console.log("cant  jump")
                }


                break;

            case getConfig()["pool"]["done"]:

                console.log("at destination position")

                break;
    
            default:
                break
                
        }
          
        if (!(t.state in this.levelState.players[player].state)) {
            console.log("not there", t.state)
            return
        }

        let stateBoundaries = this.levelState.players[player].state[t.state]

        // x,y where needs to land
        let destinationPosition = remapPosition(
            stateBoundaries.row, 
            stateBoundaries.column, 
            BoardTile
        );

        this.levelState.players[player].tokens[token].notify({
            command: "newDestination",
            destinationPosition: destinationPosition
        })
                
        return true;
    }

}

export { Level }