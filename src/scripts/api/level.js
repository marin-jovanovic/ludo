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



async function getSpecificLevel({
    levelId
}) {
    return await apiCalls.handleNewResponse(
        await apiCalls.api.get(
            `level/${levelId}`,
            apiCalls.getAuthenticationHeader()
        )
    );
}


// todo missing data
async function leaveGame(levelId) {
    return await apiCalls.handleNewResponse(
        await apiCalls.api.put(
            `level/${levelId}`,
            JSON.stringify({
                "leave": true
            }),
            apiCalls.getAuthenticationHeader()
        )
    );
}

async function joinGame(levelId) {
    return await apiCalls.handleNewResponse(
        await apiCalls.api.put(
            `level/${levelId}`,
            JSON.stringify({
                "join": true
            }),
            apiCalls.getAuthenticationHeader()
        )
    );
}

export const apiLevel = {
    createGame,
    getGames,
    leaveGame,
    joinGame,
    getSpecificLevel,

}