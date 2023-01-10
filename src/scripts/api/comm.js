import axios from 'axios'
import Cookies from 'js-cookie'
import {
    userMetaSS
} from '../session_storage';
// import {
//     apiAuth
// } from './auth';

import {
    Buffer
} from 'buffer';


const api = axios.create({
    baseURL: process.env.VUE_APP_BACKEND_URL,
    timeout: 5000,
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': Cookies.get('csrftoken')
    }
})


function encode(d) {
    // return encodeBase64(d);
    return Buffer.from(d).toString('base64');

}

function getBasicAuth({
    username,
    password
}) {
    return encode('Basic ' + username + ':' + password)
}

function getCreateAuth({
    username,
    password
}) {
    return encode('Create ' + username + ':' + password)
}

function getCustomAuth({
    username,
    accessToken
}) {
    return encode('Custom ' + username + ':' + accessToken)
}

function getAuthenticationHeader() {

    if (userMetaSS.isAuth()) {

        let credentials = userMetaSS.getCredentials();

        let username = credentials.username;
        let accessToken = credentials.accessToken;

        return {
            headers: {

                'Authorization': getCustomAuth({
                    username: username,
                    accessToken: accessToken
                })

            }
        }

    } else {

        return {
            headers: {}
        }

    }

}

function handleNewResponse(response) {

    if (!response.data.auth.status) {
        console.log("[auth] not correct")
        let t = response.data.payload;
        delete t.status;
        return t;
    }

    if (!response.data.payload.status) {
        console.log("[server] internal err")
    let t = response.data.payload;
    delete t.status;
    return t;

    }

        // todo this will never be true, not implemented
        // if (response.data.status === 401) {
        //     apiAuth.logout();
        //     location.reload(true);
        // }



    if (response.data.auth.status) {

        let accessToken = response.data.auth.accessToken;
        let username = response.data.auth.username;

        userMetaSS.login({
            username: username,
            accessToken: accessToken
        })

    } 

    let t = response.data.payload;
    delete t.status;
    return t;



}

export const apiCalls = {
    api,
    getAuthenticationHeader,
    handleNewResponse,
    getBasicAuth,
    getCreateAuth,
}