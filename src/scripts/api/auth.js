import {
    userMetaSS
} from '../session_storage';
import {
    apiCalls
} from './comm';

async function login(username, password) {

    console.log(username, password)

    const response = await apiCalls.api.post(
        `login/${username}`, {}, {
            headers: {
                'Authorization': 'Basic ' + ((encodeURIComponent(username + ':' + password)))
            }
        }
    );
    console.log(response)

    const user = await apiCalls.handleNewResponse(response);
    console.log(user)

    return user

}

async function signup(username, password) {

    console.log(username, password)
    const response = await apiCalls.api.post(
        `signup/${username}`, {}, {
            headers: {
                'Authorization': 'Create ' + ((encodeURIComponent(username + ':' + password)))
            }
        }
    );

    console.log(response)

    const user = await apiCalls.handleNewResponse(response);


    return user

}

function logout() {
    console.log('logout')

    if (userMetaSS.isAuth()) {

        let credentials = userMetaSS.getCredentials();
        let username = credentials.username;

        console.log(username)

        apiCalls.api.post(
            `logout/${username}`, {},
            apiCalls.getAuthenticationHeader()
        );

        userMetaSS.logout();
    }

}



export const apiAuth = {
    login,
    logout,
    signup
}