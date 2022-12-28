import {
    apiCalls
} from './comm';


async function getBoard(type, resource) {
    return await apiCalls.handleNewResponse(
        await apiCalls.api.get(
            `board/${type}/${resource}`,
            apiCalls.getAuthenticationHeader()
        )
    );
}


export const apiBoard = {
    getBoard,


}