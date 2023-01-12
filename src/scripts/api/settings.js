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

async function deleteAccount(username) {
    return await apiCalls.handleNewResponse(
        await apiCalls.api.delete(
            "settings/" + username,
            apiCalls.getAuthenticationHeader()
        )
    );

}

export const apiSettings = {
    updateSettings,
    getSettings,
    deleteAccount,
}