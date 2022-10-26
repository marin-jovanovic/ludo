import { apiCalls } from './comm';



async function createGame(gameName, capacity) {
    return await apiCalls.handleNewResponse(
        await apiCalls.api.post(
            `lobby/${gameName}`,
            JSON.stringify({capacity: capacity}),
            apiCalls.getAuthenticationHeader()
        )
    );

}

async function getGames() {
    return await apiCalls.handleNewResponse(
        await apiCalls.api.get(
            "lobby/",
//             {
//                 ...            JSON.stringify({"username": username}),
// ...                
//             }
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
            `lobby/${gameName}`,
            JSON.stringify({"leave": true}),
            apiCalls.getAuthenticationHeader()
        )
    );
}

async function joinGame(gameName) {
    return await apiCalls.handleNewResponse(
        await apiCalls.api.put(
            `lobby/${gameName}`,
            JSON.stringify({"join": true}),
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
