import {
    apiCalls
} from './comm';

class UserConnectionApi {
    constructor() {
        this.baseUrl = "user/"
    }

    constructUrl = ({
        connectionId
    }) => {
        return `user/connection/${connectionId}`;
    }


    getAllUsers = async () => {

        let page = 0


        return await apiCalls.handleNewResponse(
            await apiCalls.api.get(
                "user/page/" + page,
                apiCalls.getAuthenticationHeader()


            )
        );

    }




}



const userApi = new UserConnectionApi();

export {
    userApi
}