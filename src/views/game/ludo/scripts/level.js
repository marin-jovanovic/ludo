import { getMap, getPlayer1Moves } from "./api.js"
import { getBoundaries, getTokens, mapTokens } from "./layers.js"
import { Boundary } from "./boundary.js"


class Level {
    constructor() {

        // nek svak ima svoju boju, nek to pise u backendu,
        // sta kad se preklope / pojedu

        // sta kad se preklope useri

        // base layer
        let map = getMap();


        // ovo nek bude DTO
        let levelState = {
            status: {
                isGameDone: false,
                quit: ['player1'],
                won: undefined
            },
            players: {
                0: {
                    position: 'up left',
                    colour: 'green',
                    username: '1 username / nickname',
                    tokens: mapTokens({
                        map: map,
                        Boundary: Boundary,
                        colour: 'green'
                    })
                },
                1: {
                    position: 'up right',
                    colour: 'blue',
                    username: '2 username / nickname',
                    tokens: mapTokens({
                        map: map,
                        Boundary: Boundary,
                        colour: 'blue',
                        // position: 
                    })


                },
                3: {
                    position: 'down left',
                    colour: 'red',
                    username: '3 username / nickname',
                    tokens: mapTokens({
                        map: map,
                        Boundary: Boundary,
                        colour: 'red'
                    })


                },
                4: {
                    position: 'down right',
                    colour: 'yellow',
                    username: '4 username / nickname',
                    tokens: mapTokens({
                        map: map,
                        Boundary: Boundary,
                        colour: 'yellow'
                    })


                }
            }


        }

        this.status = levelState.status;
        this.players = levelState.players;

        this.player1State = getPlayer1Moves();


        // tokens
        this.tokens = getTokens({ map: map, Boundary: Boundary, })

        // board
        this.boundaries = getBoundaries({ map: map, Boundary: Boundary });

   
    }

  

}

export { Level }