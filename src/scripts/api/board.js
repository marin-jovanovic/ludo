import {
    apiCalls
} from './comm';


async function getLevel(levelId) {

    return await apiCalls.handleNewResponse(
        await apiCalls.api.get(
            `board/${levelId}`,
            apiCalls.getAuthenticationHeader()
        )
    );
}







export const apiBoard = {
    getLevel,

}