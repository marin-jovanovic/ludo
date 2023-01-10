import {
    apiCalls
} from './comm';

// async function getResource(gameId, resource) {
//     if (!(['startPool', 'moves', 'config', 'map', 'players'].includes(resource))) {
//         console.log('resource not present');
//     }

//     // console.log("getResource", gameId, resource)

//     return await apiCalls.handleNewResponse(
//         await apiCalls.api.get(
//             `board/${gameId}/${resource}`,
//             apiCalls.getAuthenticationHeader()
//         )
//     );
// }


async function getResources(gameId) {
    // if (!(['startPool', 'moves', 'config', 'map', 'players'].includes(resource))) {
    //     console.log('resource not present');
    // }

    // console.log("getResource", gameId, resource)

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