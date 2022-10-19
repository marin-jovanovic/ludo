import axios from 'axios'
import Cookies from 'js-cookie'
import { apiAuth } from './auth';

const api = axios.create({
    baseURL: 'http://localhost:8000',
    timeout: 5000,
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': Cookies.get('csrftoken')
    }
})

function get_auth_header() {
    if (sessionStorage.getItem("user") !== null) {
        let user = JSON.parse(window.sessionStorage.getItem('user'));
        let access_token = user["auth"]["access-token"]
        let refresh_token = user["auth"]["refresh-token"];

        return { headers: { 'Authorization': 'Digest ' + ((encodeURIComponent(access_token + ':' + refresh_token))) } }
    } else {
        return { headers: { 'Authorization': 'Digest ' + ((encodeURIComponent("not" + ':' + "present_err"))) } }
    }

}

function handleNewResponse(response) {

    if (!response.data.auth.status) {

        // todo api response codes
        if (response.data.status === 401) {
            apiAuth.logout();
            location.reload(true);
        } else {
            // todo check 
            // apiAuth.logout();
            // location.reload(true);

        }

        const error = "username password combination mismatchrr"
        return Promise.reject(error);
    }

    return response.data
}

export const apiCalls = {
    api,
    handleNewResponse,
    get_auth_header,
}
