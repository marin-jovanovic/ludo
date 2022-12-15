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

async function getMessages(game) {

    let params = {
        "game": game
    };

    return await apiCalls.handleNewResponse(
        await apiCalls.api.get(
            `message/${game}`,

            {
                ...apiCalls.getAuthenticationHeader(),
                ...params

            }


            // apiCalls.getAuthenticationHeader()
        )
    );
}

// // todo missing data
// async function leaveGame(gameName) {
//     return await apiCalls.handleNewResponse(
//         await apiCalls.api.put(
//             `lobby/${gameName}`,
//             JSON.stringify({"leave": true}),
//             apiCalls.getAuthenticationHeader()
//         )
//     );
// }

// async function joinGame(gameName) {
//     return await apiCalls.handleNewResponse(
//         await apiCalls.api.put(
//             `lobby/${gameName}`,
//             JSON.stringify({"join": true}),
//             apiCalls.getAuthenticationHeader()
//         )
//     );
// }

export const apiMessage = {
    // createGame,
    // getGames,
    // leaveGame,
    // joinGame

    sendMessage,
    getMessages
}