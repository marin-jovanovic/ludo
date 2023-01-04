import {
    apiCalls
} from './comm';



async function sendMessage(sender, game, content) {
    console.log("seend maesggae")
    console.log("game", game);
    return await apiCalls.handleNewResponse(
        await apiCalls.api.post(
            `message/${game}`,
            JSON.stringify({
                sender: sender,
                game: game,
                content: content
            }),
            apiCalls.getAuthenticationHeader()
        )
    );

}

async function getMessages(levelId) {
console.log("get msg", levelId);

    // let params = {
    //     "game": levelId
    // };

    return await apiCalls.handleNewResponse(
        await apiCalls.api.get(
            `message/${levelId}`,

            {
                ...apiCalls.getAuthenticationHeader(),
                // ...params

            }


            // apiCalls.getAuthenticationHeader()
        )
    );
}


export const apiMessage = {
    // createGame,
    // getGames,
    // leaveGame,
    // joinGame

    sendMessage,
    getMessages
}