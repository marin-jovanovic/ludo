import {
    apiCalls
} from './comm';

class UserConnectionApi {
    constructor() {
        this.baseUrl = "user/connection"
    }


    getAllConnections = async () => {

        // console.log("get all con")

        return await apiCalls.handleNewResponse(
            await apiCalls.api.get(
                `statistics`,
                apiCalls.getAuthenticationHeader()
            )
        );


    }



}



const statisticsApi = new UserConnectionApi();

export {
    statisticsApi
}