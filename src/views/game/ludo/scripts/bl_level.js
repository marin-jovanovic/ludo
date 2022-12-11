import { 
    remapPosition,

} from "./layers.js";
import { BoardTile } from "./ui_board_tile.js";
import { ContentCreator } from "./content_creator.js";



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

        for (const [playerId, playerMetadata] of Object.entries(players)) {


            p[playerId] = {
                        username: playerMetadata.username,

                tokens: tokens,
                state: moves[c]

            }





            // p[playerId] = {
        
            //     username: playerMetadata.username,
            //     tokens: mapTokens({
            //         map: map,
            //         Boundary: BoardTile,
            //         colour: playerMetadata.colour,
            //         // subscriber: this.onChange
            //     })[0],
            //     state: moves[c]

            // }

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


        
        // console.log(levelState);
        // console.table(levelState)

        return levelState;

    }

    movePosition({ player, token, jumpCount }) {
        /**
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

    __movePositionDriver({ player, token, jumpCount }) {

        // current token 
        let t = this.levelState.players[player].tokens[token];

        // console.log("curr token", t);

        //////////////////////////////////////////////////////
        // this is pure ui logic for moving one by one position 

        // if (this.config.configOneByOne) {

        // for (let i = t.state; i < t.state + jumpCount; i++) {
        
        //     if (i in this.levelState.players[player].state) {
        //         let stateBoundaries = this.levelState.players[player].state[i]

        //         let destinationPosition = remapPosition(
        //             stateBoundaries.column, 
        //             stateBoundaries.row, 
        //             BoardTile
        //         );

        //         // move token for jumpCount positions
        //         this.levelState.players[player].tokens[token].moveByOne({ destinationPosition: destinationPosition })

        //     } else {
        //         console.log('integrity error: not in state object')
        //     }

        // }

        // }

        //////////////////////////////////////////////////////

        // bl
        t.move({
            count: jumpCount, 
        });

        let stateBoundaries = this.levelState.players[player].state[t.state]

        // x,y where needs to land
        let destinationPosition = remapPosition(
            stateBoundaries.column, 
            stateBoundaries.row, 
            BoardTile
        );

        // console.log("dest", destinationPosition)

        // this.levelState.players[player].tokens[token].setDestionationPosition(destinationPosition)

        this.levelState.players[player].tokens[token].notify({
            command: "newDestination",
            destinationPosition: destinationPosition
        })
        
        
        // setDestionationPosition(destinationPosition)


        return true;
    }

}

export { Level }