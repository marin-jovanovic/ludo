import { remapPosition } from "./ui_comm.js";
import { BoardTile } from "./ui_board_tile.js";
import { ContentCreator } from "./content_creator.js";
import {getConfig} from "./token.js";

class Level extends ContentCreator {
    constructor({ moves, players, tokens}) {
        super();
        
        // todo check if this is DTO
        // DTO - data transfer object
        this.levelState = this.fetchLevelState({
            players: players, 
            moves: moves, 
            tokens: tokens
        });
    
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

    movePosition({ playerId, tokenId, jumpCount }) {
        /**
            todo check are performed in backend? 

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
            playerId: playerId,
            tokenId: tokenId,
            jumpCount: jumpCount,
        });

        if (isLegalMove) {

            // move token on ui layer

            let token = this.levelState.players[playerId].tokens[tokenId];

            if (!(token.state in this.levelState.players[playerId].state)) {
                console.log("err: state not in state dict");
                // assumption: token was moved to start position
                // notif: reset was called, no need to launch newDestination notif
                return;
            }

            let stateBoundaries = this.levelState.players[playerId].state[token.state];

            // x,y where needs to land
            let destinationPosition = remapPosition(
                stateBoundaries.row, 
                stateBoundaries.column, 
                BoardTile
            );
    
            token.notify({
                command: "newDestination",
                destinationPosition: destinationPosition
            })

            // move token on bl
                 
        }
   
    }

    restartToken({ playerId, tokenId }) {
        this.levelState.players[playerId].tokens[tokenId].restart();
    }

    isNotJumpingOverRestricted = ({jumpCount, player, tokenId}) => {
        /**
         * return true if can perform this jump
         * return false else
         */
        

        // we are viewing this in relative perspective

        let t = this.levelState.players[player].tokens[tokenId];
        let restrictedJumpingOver = [53, 52, 51, 50, 49, 48]; 


        if (!( restrictedJumpingOver.includes(
            (t.state + jumpCount)
        ))) {
            return true
        }

        let occupiedSpaces = [];

        for (const [t, tMeta] of Object.entries(this.levelState.players[player].tokens)) {

            if (Number(t) !== Number(tokenId)) {

                if ( restrictedJumpingOver.includes(tMeta.state)) {
                    occupiedSpaces.push(tMeta.state);
                }
            }
        }

       let lowest = Math.min(...occupiedSpaces);

       return t.state + jumpCount < lowest

    }

    isGameWon = ({playerId}) => {


        let restrictedJumpingOver = [53, 52, 51, 50]; 
        let occupiedSpaces = [];

        for (
            const tMeta of Object.values(this.levelState.players[playerId].tokens)
        ) {

                if ( restrictedJumpingOver.includes(tMeta.state)) {
                    occupiedSpaces.push(tMeta.state);
                }
        }
   
        return occupiedSpaces.length === restrictedJumpingOver.length;

    }

    checkEating = ({playerId, tokenId}) => {

        console.log();
        // absolute view
        
        let occupiedSpaces = {};
        console.log(playerId, tokenId, occupiedSpaces)

        let token = this.levelState.players[playerId].tokens[tokenId];
        
        let stateOfInteres = token.absoluteState;

        for (const [playerId, p] of Object.entries(this.levelState.players)) {

            Object.values(p.tokens).forEach(t => {

                if (t !== token) {

                    let k = playerId;

                    if (t.absoluteState === stateOfInteres) {
                 
                        if (k in occupiedSpaces) {
                            occupiedSpaces[k].push(t);
                        } else {
                            occupiedSpaces[k] = [t];
                        }
   
                    }

                }
            });

        }

        // Object.values(this.levelState.players).forEach(p => {
            
    
        // });

        console.log("tokens at this place", occupiedSpaces)


        console.log("player id", playerId)

        /*
            case 1:
                this user has any tokens here
            case 2:
                1 other user has 1 token here
                that token is removed
                this token stays
            case 3:
                1 other user has more than 1 token here
                block is formed
                this token is removed
            case 4:
                2 other users have tokens here
                if first one formed a block then all tokens from second player are removed => goto case 3

                if first one has one token and second player moves his token to this piece then the first token is remove => goto case 2

            conclusion: 
                if my tokens are here 
                    do nothing
                if other user token is here 
                    if 1
                        remove that token
                    if more then 1
                        remove this token
        */

        if (occupiedSpaces.length === 1) {
            console.log("only my tokens are here")
        } else {
            for (const [owner, tokens] of Object.entries(occupiedSpaces)) {
                console.log(owner, playerId, typeof(owner), typeof(playerId));

                console.log(Number(owner), Number(owner) !== playerId)

                if (Number(owner) !== playerId) {
                    if (tokens.length === 1) {
                        console.log("1 enemy token, perform eating");

                        tokens.forEach(t => {
                            t.restart();
                        });


                    } else if (tokens.length >= 1) {
                        console.log("enemy tokens forming a block, this token goes to start position")

                        token.restart();
                    }
                }

            }
        }

    }

    moveTokenFromStartingPoolToLivePool({token, playerId}) {
        // todo dehardcode absolute state

        token.pool = getConfig()["pool"]["live"];
        token.state = 0;
        token.absoluteState = 12 * playerId;

    }

    __movePositionDriver({ playerId, tokenId, jumpCount }) {
        /**
         * move token on business layer
         */

        if (!(playerId in this.levelState.players)) {
            console.log("err: unknown player", playerId);
            return;
        }

        if (!(tokenId in this.levelState.players[playerId].tokens)) {
            console.log("err: unknown token", tokenId);
            return;
        }

        // if (jumpCount === 0) {
        //     console.log("no movement");
        //     return;
        // }

        let token = this.levelState.players[playerId].tokens[tokenId];

        switch (token.pool) {
            case getConfig()["pool"]["start"]:
                this.moveTokenFromStartingPoolToLivePool({
                    token: token,
                    playerId: playerId
                });
                break;
            
            case getConfig()["pool"]["live"]:

                // check if can move so much 
             
                if (
                    token.state + jumpCount
                    in this.levelState.players[playerId].state
                ) {
                    // state exists

                    if (this.isNotJumpingOverRestricted({
                        jumpCount: jumpCount, 
                        player: playerId, 
                        tokenId: tokenId
                    })) {

                        // bl
                        token.move({
                            count: jumpCount, 
                        });

                    }else {
                        console.log("can not jump over other token in restricted jumping area")
                    }

                } else {
                    console.log("ret false")
                    // return false;
                }

                break;

            case getConfig()["pool"]["done"]:

                // todo add logic that add this token to done pool
                console.log("at destination position")

                break;
    
            default:

                console.log("err: unknown")
                break
                
        }
          
        if (!(token.state in this.levelState.players[playerId].state)) {
            console.log("err not there", token.state)
            return
        }


        if (this.isGameWon({playerId: playerId})) {
            console.log("todo game won");
        } 

        this.checkEating({
            playerId: playerId,
            tokenId: tokenId
        });


        return true;
    }

}

export { Level }