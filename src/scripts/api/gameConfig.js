import {
    apiCalls
} from './comm';



async function getResources(gameId) {

    return await apiCalls.handleNewResponse(
        await apiCalls.api.get(
            `board/${gameId}`,
            apiCalls.getAuthenticationHeader()
        )
    );
}


export const apiGameConfig = {
    getResources,
}