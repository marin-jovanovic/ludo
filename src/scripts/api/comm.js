import axios from 'axios'
import Cookies from 'js-cookie'
import {
    apiAuth
} from './auth';

const api = axios.create({
    baseURL: 'http://localhost:8000',
    timeout: 5000,
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': Cookies.get('csrftoken')
    }
})

function getAuthenticationHeader() {
    let username = sessionStorage.getItem("username");
    let accessToken = sessionStorage.getItem("accessToken")

    if (username && accessToken) {


        return {
            headers: {
                'Authorization': 'Custom ' + ((encodeURIComponent(username + ':' + accessToken)))
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

        sessionStorage.setItem('username', username);

        sessionStorage.setItem('accessToken', accessToken);

    } else {
        // todo this will never be true, not implemented
        if (response.data.status === 401) {
            apiAuth.logout();
            location.reload(true);
        }

        const error = response.data.payload.debug;
        return Promise.reject(error);
    }

    return response.data
}

export const apiCalls = {
    api,
    getAuthenticationHeader,
    handleNewResponse,
}