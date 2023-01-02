import {
    apiCalls
} from './comm';



async function createGame(gameName, capacity) {
    return await apiCalls.handleNewResponse(
        await apiCalls.api.post(
            `level/${gameName}`,
            JSON.stringify({
                capacity: capacity
            }),
            apiCalls.getAuthenticationHeader()
        )
    );

}

async function getGames() {
    return await apiCalls.handleNewResponse(
        await apiCalls.api.get(
            "level/",

            apiCalls.getAuthenticationHeader()

        )
    );
}

// async function getSpecificGame(name) {
//     return await apiCalls.handleNewResponse(
//         await apiCalls.api.get(
//             `lobby/${name}`,
//             apiCalls.getAuthenticationHeader()
//         )
//     );
// }


// todo missing data
async function leaveGame(gameName) {
    return await apiCalls.handleNewResponse(
        await apiCalls.api.put(
            `level/${gameName}`,
            JSON.stringify({
                "leave": true
            }),
            apiCalls.getAuthenticationHeader()
        )
    );
}

async function joinGame(gameName) {
    return await apiCalls.handleNewResponse(
        await apiCalls.api.put(
            `level/${gameName}`,
            JSON.stringify({
                "join": true
            }),
            apiCalls.getAuthenticationHeader()
        )
    );
}

export const apiLobby = {
    createGame,
    getGames,
    leaveGame,
    joinGame,
    // getSpecificGame,

}