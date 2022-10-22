import { apiCalls } from './comm';

async function createGame(gameName, capacity) {
    return await apiCalls.handleNewResponse(
        await apiCalls.api.post(
            `game/${gameName}`,
            JSON.stringify({capacity: capacity}),
            apiCalls.getAuthenticationHeader()
        )
    );

}

async function getGames() {
    return await apiCalls.handleNewResponse(
        await apiCalls.api.get(
            "game/",
            apiCalls.getAuthenticationHeader()
        )
    );
}

// todo missing data
async function leaveGame(gameName) {
    return await apiCalls.handleNewResponse(
        await apiCalls.api.put(
            `game/${gameName}`,
            JSON.stringify({"leave": true}),
            apiCalls.getAuthenticationHeader()
        )
    );
}

async function joinGame(gameName) {
    return await apiCalls.handleNewResponse(
        await apiCalls.api.put(
            `game/${gameName}`,
            JSON.stringify({"join": true}),
            apiCalls.getAuthenticationHeader()
        )
    );
}

export const apiLobby = {
    createGame,
    getGames,
    leaveGame,
    joinGame

}
