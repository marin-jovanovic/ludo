import {
    apiCalls
} from './comm';


// import {
//     musicSS
// } from "./../session_storage.js"

async function getMusic() {
    // return await handleNewResponse(
        await apiCalls.api.get(
            "music/",

            apiCalls.getAuthenticationHeader()

        )
    // );
}





export const apiMusic = {
    getMusic,
}