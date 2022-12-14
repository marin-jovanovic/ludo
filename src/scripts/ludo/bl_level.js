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

        levelState
    }) {
        super();

        //  todo check if this is loading properly when passed updated dto (mid game)

        // DTO - data transfer object
        this.levelState = levelState;

        // console.log(levelState);

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
            // console.log("[err] empty")
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
            console.log(this.levelState.players)
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
        let pastState = token.currentState;

        let states = this.levelState.players[playerId].state;


        switch (token.poolType) {
            case getConfig()["pool"]["start"]:

                if (jumpCount !== 1) {
                    console.log("err: must be 1 if going from start pool")
                }

                token.moveTokenFromStartingPoolToLivePool({
                    states: states
                });

                break;

            case getConfig()["pool"]["live"]:

                // check if can move so much 

                if (
                    token.currentState + jumpCount in this.levelState.players[playerId].state
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
                            states: states
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

        if (!(token.currentState in this.levelState.players[playerId].state)) {
            console.log("err not there", token.currentState)
            return
        }

        // /////////////////// notify UI ////////////////////////

        let destinationState = token.currentState;

        let history = [];
        for (let i = pastState + 1; i < destinationState + 1; i++) {
            history.push(i);
        }

        // state machine pattern
        // let states = this.levelState.players[playerId].state;

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

        let thisMovePath = [token.startXY];




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

        let token = this.levelState.players[player].tokens[tokenId];

        let states = this.levelState.players[player].state;

        let restrictedJumpingOver = this.getRestricted({
            states: states
        });


        if (!(restrictedJumpingOver.includes(
                (token.currentState + jumpCount)
            ))) {
            return true
        }

        let occupiedSpaces = [];

        for (const [t, tMeta] of Object.entries(this.levelState.players[player].tokens)) {

            if (Number(t) === Number(tokenId)) {
                continue;
            }

            if (Number(tMeta.currentState) < Number(token.currentState)) {
                continue;
            }

            if (restrictedJumpingOver.includes(tMeta.currentState)) {
                occupiedSpaces.push(tMeta.currentState);
            }
        }

        let lowest = Math.min(...occupiedSpaces);

        return token.currentState + jumpCount < lowest

    }

    getRestricted = ({
        states
    }) => {
        let restrictedJumpingOver = [];

        let restrictedEnum = "3"

        for (const [stateId, stateMeta] of Object.entries(states)) {
            if (stateMeta.type === restrictedEnum) {
                restrictedJumpingOver.push(Number(stateId))
            }
        }

        return restrictedJumpingOver;
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

        let states = this.levelState.players[playerId].state;

        let restrictedJumpingOver = this.getRestricted({
            states: states
        });

        let tokenCount = Object.keys(this.levelState.players[playerId].tokens).length;

        let last_n = restrictedJumpingOver.slice(-tokenCount);


        for (
            const tMeta of Object.values(this.levelState.players[playerId].tokens)
        ) {

            if (!(last_n.includes(tMeta.currentState))) {
                return false;
            }

        }

        return true;


    }

    checkEating = ({
        playerId,
        tokenId
    }) => {

        /**
         * assumption: this token performed move
         * 
         * on this tile we can have
         * 
         * 1 my token/s
         * 
         * 2 one enemy token
         * 
         * 3 multiple enemy tokens
         * 
         */


        // playerId => [{token, tokenId}]
        // filtered only on stateOfInteres
        let occupiedSpaces = {};

        let token = this.levelState.players[playerId].tokens[tokenId];


        for (const [playerId, p] of Object.entries(this.levelState.players)) {
            // for each player

            for (const [tokenId, currToken] of Object.entries(p.tokens)) {
                // for each token they have

                if (!(currToken.currentXY.row === token.currentXY.row &&
                        currToken.currentXY.column === token.currentXY.column
                    )) {
                    continue;
                }

                if (currToken === token) {
                    // skip current token
                    continue;
                }


                if (playerId in occupiedSpaces) {
                    occupiedSpaces[playerId].push(tokenId);
                } else {
                    occupiedSpaces[playerId] = [tokenId];
                }

            }

        }


        /*

            if mine 
                return
            if one enemy
                eat
            if more than one enemy
                return my token


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

        if (Object.keys(occupiedSpaces).length === 0) {
            // if (occupiedSpaces.length !== 1) {

            // think when nothing to rem
            // console.log("err")
            return;
        }



        if (Object.keys(occupiedSpaces).length !== 1) {

            console.log("err")
        }

        // console.log(occupiedSpaces)

        for (const [owner, tokens] of Object.entries(occupiedSpaces)) {

            if (Number(owner) !== Number(playerId)) {
                if (tokens.length === 1) {

                    // eat

                    // console.log("eat")
                    // console.log(this.levelState)




                    tokens.forEach(t => {

                        // console.log(owner, t, "eaten by", playerId, tokenId)

                        this.restartToken({
                            playerId: Number(owner),
                            tokenId: t
                        })


                    });

                } else if (tokens.length > 1) {

                    console.log("this token")

                    // this token
                    this.restartToken({
                        playerId: playerId,
                        tokenId: tokenId
                    })

                }
            }

        }



    }




}

export {
    Level
}