import {
    userMetaSS
} from '../session_storage';
import {
    apiCalls
} from './comm';
// import { Buffer } from 'buffer';
// function encodeBase64(data)  {
//     return Buffer.from(data).toString('base64');
//   }

async function login(username, password) {

    console.log(username, password)

    const response = await apiCalls.api.post(
        `login/${username}`, {}, {
            headers: {
 
                'Authorization': apiCalls.getBasicAuth({username: username, password: password})
 
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
    console.log(apiCalls.getCreateAuth({username: username, password:password}))

    const response = await apiCalls.api.post(
        `signup/${username}`, {}, {
            headers: {


                'Authorization': apiCalls.getCreateAuth({username: username, password:password})


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