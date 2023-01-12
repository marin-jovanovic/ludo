import {
    apiCalls
} from './comm';

class UserConnectionApi {
    constructor() {
        this.baseUrl = "user/profilePhoto"
    }

    constructUrl = ({
        connectionId
    }) => {
        return `user/connection/${connectionId}`;
    }


    getProfilePhoto = async ({
        userId
    }) => {

        return await apiCalls.handleNewResponse(
            await apiCalls.api.get(
                this.baseUrl + "/" + userId,
                apiCalls.getAuthenticationHeader()
            )
        );

    }


}



const userProfilePhoto = new UserConnectionApi();

export {
    userProfilePhoto
}