import { 
    mapTokens,
    remapPosition,

} from "./layers.js";
import { BoardTile } from "./ui_board_tile.js";
import { ContentCreator } from "./content_creator.js";


class Level extends ContentCreator {
    constructor(map, moves, players) {
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
        this.levelState = this.fetchLevelState(players, map);

        // todo remove, parametrize
        this.player1State = moves[0];
    
    }

    start() {
        this.notify({
            command: "drawBoard"
        });

        this.notify({
            command: "animateTokens", 
            level: this, 
        });

    }

    // rewrite
    fetchLevelState(players, map) {
        let p = {};

        for (const [playerId, playerMetadata] of Object.entries(players)) {

            p[playerId] = {
        
                username: playerMetadata.username,
                tokens: mapTokens({
                    map: map,
                    Boundary: BoardTile,
                    subscriber: this.onChange
                })
            }

        }

        let levelState = {
            status: {
                isGameDone: false,
                quit: ['player1'],
                won: undefined
            },
            players: p
        }

        return levelState;

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

    onChange() {

        console.log("on change")

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

    __movePositionDriver({ player, token, jumpCount }) {
        let t = this.levelState.players[player].tokens[token];

        if (this.config.configOneByOne) {

            for (let i = t.state; i < t.state + jumpCount; i++) {

                if (i in this.player1State) {
                    let stateBoundaries = this.player1State[i]

                    let destinationPosition = remapPosition(
                        stateBoundaries.column, 
                        stateBoundaries.row, 
                        BoardTile
                    );

                    this.levelState.players[player].tokens[token].moveByOne({ destinationPosition: destinationPosition })

                } else {
                    console.log('integrity error: not in state object')
                }

            }

        }

        t.state += jumpCount

        let stateBoundaries = this.player1State[t.state]

        let destinationPosition = remapPosition(
            stateBoundaries.column, 
            stateBoundaries.row, 
            BoardTile
        );

        this.levelState.players[player].tokens[token].setDestionationPosition(destinationPosition)

    }

    __restartToken({ player, token }) {
        this.levelState.players[player].tokens[token].restart();

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