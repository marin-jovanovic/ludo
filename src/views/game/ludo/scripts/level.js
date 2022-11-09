// import { getMap, getPlayer1Moves } from "./api.js"
import { getBoundaries, getTokens, mapTokens } from "./layers.js"
import { Boundary } from "./boundary.js"


class Level {
    constructor(map, moves, players) {

        // todo extract colour to config
        // 

        // sta kad se preklope / pojedu

        // sta kad se preklope useri, (two users at same tile)

        let p = {};

        for (const [key, value] of Object.entries(players)) {
            console.log(key, value);

            p[key] = {
                // todo check if needed
                // position: 'up left',
                colour: value.colour,
                username: value.username,
                tokens: mapTokens({
                    map: map,
                    Boundary: Boundary,
                    colour: value.colour
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

        this.tokens = getTokens({ map: map, Boundary: Boundary, })

        // board
        this.boundaries = getBoundaries({ map: map, Boundary: Boundary });
    }
}

export { Level }