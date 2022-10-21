import { apiCalls } from './comm';

async function createGame(gameName, capacity) {
    return await apiCalls.handleNewResponse(
        await apiCalls.api.post(
            `game/${gameName}`,
            JSON.stringify(capacity),
            apiCalls.get_auth_header()
        )
    );

}

async function getGames() {
    return await apiCalls.handleNewResponse(
        await apiCalls.api.get(
            "game/",
            apiCalls.get_auth_header()
        )
    );
}

// todo missing data
async function leaveGame(gameName) {
    return await apiCalls.handleNewResponse(
        await apiCalls.api.get(
            `game/${gameName}`,
            apiCalls.get_auth_header()
        )
    );
}

async function joinGame() {

}

export const apiLobby = {
    createGame,
    getGames,
    leaveGame,
    joinGame

}
