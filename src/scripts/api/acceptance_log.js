import {
    apiCalls
} from './comm';

class AcceptanceLogApi {
    constructor() {
        this.baseUrl = "level"
    }

    constructUrl = ({
        levelId
    }) => {
        return `level/${levelId}/acceptanceLog`;
    }

    addEntryToAcceptanceLog = async ({
        levelId,
        entryId,
        payload = undefined
    }) => {

        return await apiCalls.handleNewResponse(
            await apiCalls.api.post(
                this.constructUrl({
                    levelId: levelId
                }) + "/" + entryId,

                // `${this.baseUrl}/${levelId}/acceptanceLog`,
                JSON.stringify({
                    // entryId: entryId,
                    payload: payload
                }),
                apiCalls.getAuthenticationHeader()
            )
        );


    }

    getAcceptanceLogForLevel = async ({
        levelId
    }) => {

        return await apiCalls.handleNewResponse(
            await apiCalls.api.get(
                this.constructUrl({
                    levelId: levelId
                }),

                // `${this.baseUrl}/${levelId}/acceptanceLog`,
                // JSON.stringify({
                //     // entryId: entryId,
                //     // payload: payload
                // }),
                apiCalls.getAuthenticationHeader()
            )
        );


    }


}


// async function getLevelLog(game) {

//     console.log("get game", game)

//     return await apiCalls.handleNewResponse(
//         await apiCalls.api.get(
//             `acceptanceLog/${game}/log`,
//             apiCalls.getAuthenticationHeader()
//         )
//     );
// }

const acceptanceLogApi = new AcceptanceLogApi();

export {
    acceptanceLogApi
}

