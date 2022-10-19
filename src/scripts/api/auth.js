import { apiCalls } from './comm';

async function login(username, password) {

    const response = await apiCalls.api.post(
        `login/${username}`,
        {},
        {
            headers: {
                'Authorization': 'Basic ' + ((encodeURIComponent(username + ':' + password)))
            }
        }
    );

    const user = await apiCalls.handleNewResponse(response)
    if (user) {
        sessionStorage.setItem('user', JSON.stringify(user));
    }
    return user

}

function logout() {
    if (sessionStorage.getItem("user") !== null) {
        apiCalls.api.post(
            "logout/",
            {},
            apiCalls.get_auth_header()
        );
        sessionStorage.removeItem('user');

    }

}

export const apiAuth = {
    login,
    logout
}