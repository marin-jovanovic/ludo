import {
    apiCalls
} from './comm';

class UserConnectionApi {
    constructor() {
        this.baseUrl = "user/connection"
    }

    constructUrl = ({
        connectionId
    }) => {
        return `user/connection/${connectionId}`;
    }


    getAllConnections = async () => {

        return await apiCalls.handleNewResponse(
            await apiCalls.api.get(
                this.baseUrl,        
                apiCalls.getAuthenticationHeader()
            )
        );


    }

    sendConnectionRequest = async ({
        userId
    }) => {

        return await apiCalls.handleNewResponse(
            await apiCalls.api.post(
                `user/connection/${userId}`,
                JSON.stringify({
                    payload: {
                        send: true
                    }
                }),
                apiCalls.getAuthenticationHeader()
            )
        );


    }


}



const userConnectionApi = new UserConnectionApi();

export {
    userConnectionApi
}

