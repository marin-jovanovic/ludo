import {
    apiCalls
} from './comm';

class UserConnectionApi {
    constructor() {
        this.baseUrl = "directMessage/"
    }



    getMessages = async (userId) => {

        return await apiCalls.handleNewResponse(
            await apiCalls.api.get(
                this.baseUrl + userId,
                apiCalls.getAuthenticationHeader()
            )
        );


    }

    sendMessage = async ({
        userId, content
    }) => {

        return await apiCalls.handleNewResponse(
            await apiCalls.api.post(
                this.baseUrl + userId,
                JSON.stringify({
                      content: content
              
                }),
                apiCalls.getAuthenticationHeader()
            )
        );


    }


}



const directMessagesApi = new UserConnectionApi();

export {
    directMessagesApi
}