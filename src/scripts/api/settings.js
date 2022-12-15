import {
    apiCalls
} from './comm';



async function updateSettings(settings) {
    return await apiCalls.handleNewResponse(
        await apiCalls.api.post(
            "settings/",
            JSON.stringify(settings),
            apiCalls.getAuthenticationHeader()
        )
    );

}

async function getSettings() {
    return await apiCalls.handleNewResponse(
        await apiCalls.api.get(
            "settings/",
            apiCalls.getAuthenticationHeader()
        )
    );
}

export const apiSettings = {
    updateSettings,
    getSettings,

}