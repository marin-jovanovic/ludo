import {
    ContentCreator
} from "./content_creator.js";
import {
    getConfig
} from "./bl_token.js";

/**
 * public
 * 
 * @movePosition
 * @restartToken
 * 
 * when ui updated call @updated
 * 
 * when trying to update ui call @tryToSend
 * 
 */

class Level extends ContentCreator {
    constructor({
        moves,
        players,
        tokens
    }) {
        super();

        // todo check if this is DTO
        // DTO - data transfer object
        this.levelState = this.fetchLevelState({
            players: players,
            moves: moves,
            tokens: tokens
        });

        // this is for notifying bl
        this.changleLog = [];
        this.isWaitingForAcceptance = false;
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
        });

    }

    // todo rewrite
    fetchLevelState({
        players,
        moves,
        tokens
    }) {
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

    updated = () => {
        /**
         * callback for updating ui
         */

        // todo check for race condition

        if (this.changleLog.length === 0) {

            this.isWaitingForAcceptance = false;

        } else {

            let oldest = this.changleLog[0];

            let oldestMove = oldest.move;
            let oldestToken = oldest.token;

            oldestToken.notify({
                command: "newDestination",
                diff: oldestMove
            })

            this.changleLog.shift();

        }

    }

    // safe send
    tryToSend = ({
        playerId,
        tokenId,
        thisMovePath
    }) => {

        if (!thisMovePath?.length) {
            console.log("[err] empty")
            return;
        }


        /**
         * if can notify
         * set flag that it can not notify
         * 
         * if log is empty
         * notify this change
         * 
         * else 
         * notify oldest change
         * remove oldest change from log
         * add this change to log
         *  
         * else 
         * add this change to log
         * 
         */

        // current token
        let token = this.levelState.players[playerId].tokens[tokenId];

        if (!this.isWaitingForAcceptance) {
            this.isWaitingForAcceptance = true;

            if (this.changleLog.length === 0) {
                // send current

                token.notify({
                    command: "newDestination",
                    diff: thisMovePath
                })

            } else {

                // send oldest, log current

                let oldest = this.changleLog.shift();

                let oldestMove = oldest.move;
                let oldestToken = oldest.token;

                oldestToken.notify({
                    command: "newDestination",
                    diff: oldestMove
                })

                this.changleLog.push({
                    token: token,
                    move: thisMovePath
                });

            }

        } else {

            // log current

            this.changleLog.push({
                token: token,
                move: thisMovePath
            });

        }

    }

    movePosition({
        playerId,
        tokenId,
        jumpCount
    }) {
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



        if (!(playerId in this.levelState.players)) {
            console.log("err: unknown player", playerId);
            return;
        }

        if (!(tokenId in this.levelState.players[playerId].tokens)) {
            console.log("err: unknown token", tokenId);
            return;
        }

        if (jumpCount === 0) {
            console.log("err: no movement");
            return;
        }

        let token = this.levelState.players[playerId].tokens[tokenId];
        let pastState = token.state;

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
                    token.state + jumpCount in this.levelState.players[playerId].state
                ) {
                    // state exists

                    if (this.isNotJumpingOverRestricted({
                            jumpCount: jumpCount,
                            player: playerId,
                            tokenId: tokenId
                        })) {

                        // not jumping over restricted 

                        token.move({
                            count: jumpCount,
                        });

                    } else {
                        console.log("err: trying to jump in restricted jumping area")
                    }

                } else {
                    console.log("err: trying to move to undefined state")
                    console.log(token)
                    console.log(this.levelState.players)

                    return;
                }

                break;

            case getConfig()["pool"]["done"]:

                // todo add logic that add this token to done pool
                console.log("at destination position")

                break;

            default:

                console.log("err: unknown pool")
                break

        }

        if (!(token.state in this.levelState.players[playerId].state)) {
            console.log("err not there", token.state)
            return
        }

        // /////////////////// notify UI ////////////////////////

        let destinationState = token.state;

        let history = [];
        for (let i = pastState + 1; i < destinationState + 1; i++) {
            history.push(i);
        }

        // state machine pattern
        let states = this.levelState.players[playerId].state;

        // // subset of states where this token traversed
        let thisMovePath = history.map(i => states[i]);

        this.tryToSend({
            playerId: playerId,
            tokenId: tokenId,
            thisMovePath: thisMovePath,
        });

        // /////////////////// checks ////////////////////////

        this.checkEating({
            playerId: playerId,
            tokenId: tokenId
        });

        if (this.isGameWon({
                playerId: playerId
            })) {
            console.log("todo game won");
        }

    }

    restartToken = ({
        playerId,
        tokenId
    }) => {
        /**
         * just a wrapper
         */


        // move this token
        // then check for moving

        this.levelState.players[playerId].tokens[tokenId].restart();

        // current token
        let token = this.levelState.players[playerId].tokens[tokenId];

        let thisMovePath = [token.boardXYPosition];
      
        this.tryToSend({
            playerId: playerId,
            tokenId: tokenId,
            thisMovePath: thisMovePath
        });

    }

    /**
     * 
     * todo dehardcode 
     * 
     * @param {*} param0 
     * @returns 
     */
    isNotJumpingOverRestricted = ({
        jumpCount,
        player,
        tokenId
    }) => {
        /**
         * return true if can perform this jump
         * return false else
         */


        // we are viewing this in relative perspective

        let t = this.levelState.players[player].tokens[tokenId];
        let restrictedJumpingOver = [53, 52, 51, 50, 49, 48];


        if (!(restrictedJumpingOver.includes(
                (t.state + jumpCount)
            ))) {
            return true
        }

        let occupiedSpaces = [];

        for (const [t, tMeta] of Object.entries(this.levelState.players[player].tokens)) {

            if (Number(t) !== Number(tokenId)) {

                if (restrictedJumpingOver.includes(tMeta.state)) {
                    occupiedSpaces.push(tMeta.state);
                }
            }
        }

        let lowest = Math.min(...occupiedSpaces);

        return t.state + jumpCount < lowest

    }

    /**
     * 
     * todo dehardcode 
     * 
     * @param {*} param0 
     * @returns 
     */
    isGameWon = ({
        playerId
    }) => {


        let restrictedJumpingOver = [53, 52, 51, 50];
        let occupiedSpaces = [];

        for (
            const tMeta of Object.values(this.levelState.players[playerId].tokens)
        ) {

            if (restrictedJumpingOver.includes(tMeta.state)) {
                occupiedSpaces.push(tMeta.state);
            }
        }

        return occupiedSpaces.length === restrictedJumpingOver.length;

    }

    checkEating = ({
        playerId,
        tokenId
    }) => {

        // absolute view

        // playerId => [{token, tokenId}]
        // filtered only on stateOfInteres
        let occupiedSpaces = {};

        let token = this.levelState.players[playerId].tokens[tokenId];

        // where @token is now
        let stateOfInteres = token.absoluteState;

        for (const [playerId, p] of Object.entries(this.levelState.players)) {

            for (const [tokenId, t] of Object.entries(p.tokens)) {

                if (t !== token) {

                    let k = playerId;

                    if (t.absoluteState === stateOfInteres) {

                        if (k in occupiedSpaces) {
                            occupiedSpaces[k].push({
                                token: t,
                                tokenId: tokenId
                            });
                        } else {
                            occupiedSpaces[k] = [{
                                token: t,
                                tokenId: tokenId
                            }];
                        }

                    }

                }

            }

        }

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

        if (occupiedSpaces.length !== 1) {
            for (const [owner, tokens] of Object.entries(occupiedSpaces)) {

                if (Number(owner) !== playerId) {
                    if (tokens.length === 1) {

                        // eat

                        tokens.forEach(t => {

                            this.restartToken({
                                playerId: Number(owner),
                                tokenId: t.tokenId
                            })


                        });

                    } else if (tokens.length > 1) {

                        this.restartToken({
                            playerId: Number(owner),
                            tokenId: tokenId
                        })


                    }
                }

            }
        }

    }

    moveTokenFromStartingPoolToLivePool({
        token,
        playerId
    }) {
        // todo dehardcode absolute state

        token.setPool({pool: getConfig()["pool"]["live"]});
        token.state = 0;
        token.absoluteState = 13 * playerId;

    }


}

export {
    Level
}