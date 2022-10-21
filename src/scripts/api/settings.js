import { apiCalls } from './comm';



async function updateSettings(settings) {
    return await apiCalls.handleNewResponse(
        await apiCalls.api.post(
            "settings/",
            JSON.stringify(settings),
            apiCalls.get_auth_header()
        )
    );

}

async function getSettings() {
    console.log("get s")
    return await apiCalls.handleNewResponse(
        await apiCalls.api.get(
            "settings/",
            apiCalls.get_auth_header()
        )
    );
}

export const apiSettings = {
    updateSettings,
    getSettings,

}
