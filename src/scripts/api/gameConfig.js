import { apiCalls } from './comm';

async function getResource(gameId, resource) {
    if (!(['startPool', 'moves', 'config', 'map'].includes(resource))) {
        console.log('resource not present');
    }

    return await apiCalls.handleNewResponse(
        await apiCalls.api.get(
            `board/${gameId}/${resource}`,
            apiCalls.getAuthenticationHeader()
        )
    );
}

export const apiGameConfig = {
    getResource,
}
