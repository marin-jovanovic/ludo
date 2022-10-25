import { apiCalls } from './comm';


async function getGame(game) {
    return await apiCalls.handleNewResponse(
        await apiCalls.api.get(
            `game/${game}`,
            apiCalls.getAuthenticationHeader()
        )
    );
}

async function updateGame(game, player, token, action) {
    console.log("action", action)

    return await apiCalls.handleNewResponse(
        await apiCalls.api.post(
            `game/${game}`,
            JSON.stringify({
                player: player,
                token: token,
                action: action
            }),
            apiCalls.getAuthenticationHeader()
        )
    );

}



export const apiGame = {
getGame,
updateGame    

}
