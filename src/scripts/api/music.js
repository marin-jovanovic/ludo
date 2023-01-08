import {
    apiCalls
} from './comm';


// import {
//     musicSS
// } from "./../session_storage.js"

async function getMusic() {
    return await handleNewResponse(
        await apiCalls.api.get(
            "music/",

            apiCalls.getAuthenticationHeader()

        )
    );
}


function handleNewResponse(response) {

    // console.log(response)

    // let data = response.data
    // console.log(data)


    // musicSS.set({value: data});

    return response

    // if (response.data.auth.status) {

    //     let accessToken = response.data.auth.accessToken;
    //     let username = response.data.auth.username;

    //     userMetaSS.login({
    //         username: username,
    //         accessToken: accessToken
    //     })


    // } else {
    //     // todo this will never be true, not implemented
    //     if (response.data.status === 401) {
    //         apiAuth.logout();
    //         location.reload(true);
    //     }

    //     const error = response.data.payload.description;
    //     return Promise.reject(error);
    // }

    // return response.data
}



export const apiMusic = {
    getMusic,
}