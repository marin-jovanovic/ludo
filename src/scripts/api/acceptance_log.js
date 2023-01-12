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


                apiCalls.getAuthenticationHeader()
            )
        );


    }


}



const acceptanceLogApi = new AcceptanceLogApi();

export {
    acceptanceLogApi
}