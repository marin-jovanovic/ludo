import {
    apiCalls
} from './comm';


async function getLevelLog(game) {


    return await apiCalls.handleNewResponse(
        await apiCalls.api.get(
            `level/${game}/log`,
            apiCalls.getAuthenticationHeader()
        )
    );
}



async function updateGame(game, player, token, action) {

    return await apiCalls.handleNewResponse(
        await apiCalls.api.post(
            `level/${game}/log`,
            JSON.stringify({
                player: player,
                token: token,
                action: action
            }),
            apiCalls.getAuthenticationHeader()
        )
    );

}

async function actionPerformed(game, player, instruction_id) {
    // todo type check before fetching

// todo i think this is not used


    return await apiCalls.handleNewResponse(
        await apiCalls.api.put(
            `level/${game}/log`,
            JSON.stringify({
                player: player,
                instructionId: instruction_id,
            }),
            apiCalls.getAuthenticationHeader()
        )
    );

}


async function addToLog(levelId, tokenId) {
    
    return await apiCalls.handleNewResponse(
        await apiCalls.api.put(
            `level/${levelId}/log`,
            JSON.stringify({
                tokenId: tokenId
            }),
            apiCalls.getAuthenticationHeader()
        )
    );

}



export const apiLevelLog = {
    getLevelLog,
    updateGame,
    actionPerformed,
    addToLog
}