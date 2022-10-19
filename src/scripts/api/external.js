import { apiCalls } from './comm';

async function getCoordinates() {

    let response = await apiCalls.api.get(`https://ipapi.co/json/`);
    response = response["data"];

    return {
        latitude: response["latitude"],
        longitude: response["longitude"]
    }

}


export const apiExternal = {
    getCoordinates
}