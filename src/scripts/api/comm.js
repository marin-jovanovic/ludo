import axios from 'axios'
import Cookies from 'js-cookie'
import {
    userMetaSS
} from '../session_storage';
import {
    apiAuth
} from './auth';

import {
    Buffer
} from 'buffer';


const api = axios.create({
    baseURL: 'http://localhost:8000',
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

    if (response.data.auth.status) {

        let accessToken = response.data.auth.accessToken;
        let username = response.data.auth.username;

        userMetaSS.login({
            username: username,
            accessToken: accessToken
        })


    } else {
        // todo this will never be true, not implemented
        if (response.data.status === 401) {
            apiAuth.logout();
            location.reload(true);
        }

        const error = response.data.payload.description;
        return Promise.reject(error);
    }

    return response.data
}

export const apiCalls = {
    api,
    getAuthenticationHeader,
    handleNewResponse,
    getBasicAuth,
    getCreateAuth,
}