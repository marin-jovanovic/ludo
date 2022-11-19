import { getBoundaries as getBoardTiles,  mapTokens } from "./layers.js"
import { BoardTile } from "./board_tile.js"
import { ContentCreator } from "./content_creator.js";


class Level extends ContentCreator {
    constructor(map, moves, players, subsFunction) {
        super();

        // todo what is this used for?
        this.configOneByOne = true;

        // wait for one token to reach destination (stops moving) before other token can be moved on board
        this.backlog = [];
        this.useBacklog = false;


        // todo extract colour to config
        // 

        // sta kad se preklope / pojedu

        // sta kad se preklope useri, (two users at same tile)

        let p = {};


        for (const [key, value] of Object.entries(players)) {
            // console.log(key, value);

            p[key] = {
        
                colour: value.colour,
                username: value.username,
                tokens: mapTokens({
                    map: map,
                    Boundary: BoardTile,
                    colour: value.colour,
                    subscriber: subsFunction
                                
                })
            }
        }

        // ovo nek bude DTO
        let levelState = {
            status: {
                isGameDone: false,
                quit: ['player1'],
                won: undefined
            },
            players: p
        }

        this.status = levelState.status;
        this.players = levelState.players;

        // todo remove, parametrize
        this.player1State = moves[0];

        // board
        this.boardTiles = getBoardTiles({ map: map, Boundary: BoardTile });
    
        // this.start();
    }

    start() {
        console.log("st")
        this.notify({command: "animateOnce", level: this, tmp: "test tmp"});

        this.notify({command: "animateLoop", level: this, tmp: "test tmp"});


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



    // notify() {
    //     this.backlog.shift();
  
    //     if (this.backlog.length === 0) {
    //       return;
    //     }
  
    //     let first = this.backlog[0];
  
    //     // todo fix, add param for action, or multiple queues
    //     if (first.length === 2) {
    //       this.moveTokenToStart({ player: first[0], token: first[1] });
    //     } else {
    //       this.movePosition({
    //         player: first[0],
    //         token: first[1],
    //         jumpCount: first[2],
    //       });
    //     }
    //   }



    _tileToCoordinates(stateBoundaries) {
        // tile (x,y) to coordinate (pixels x,y ?) 
        // find center of that pixels posiiton return it

        // todo extract
        return {
            x: stateBoundaries.column * BoardTile.width + BoardTile.width / 2,
            y: stateBoundaries.row * BoardTile.height + BoardTile.height / 2
        };

    }

    __movePositionDriver({ player, token, jumpCount }) {
        let t = this.players[player].tokens[token];

        if (this.configOneByOne) {

            for (let i = t.state; i < t.state + jumpCount; i++) {

                if (i in this.player1State) {
                    let stateBoundaries = this.player1State[i]

                    let destinationPosition = this._tileToCoordinates(stateBoundaries);

                    this.players[player].tokens[token].moveByOne({ destinationPosition: destinationPosition })

                } else {
                    console.log('integrity error: not in state object')
                }

            }

        }

        t.state += jumpCount

        let stateBoundaries = this.player1State[t.state]

        let destinationPosition = this._tileToCoordinates(stateBoundaries);

        this.players[player].tokens[token].setDestionationPosition(destinationPosition)

    }

    __restartToken({ player, token }) {
        this.players[player].tokens[token].restart();

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

export { Level }