import { apiCalls } from './comm';

async function getCSRFAuthData() {

    return await apiCalls.handleNewResponse(
        await apiCalls.api.post(
            "csrf/",
            {},
            apiCalls.get_auth_header()
        )
    );

}

export const apiCsrf = {
    getCSRFAuthData
}