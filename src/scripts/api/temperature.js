import { apiCalls } from './comm';

async function addTemperature(portfolio, section, type, value) {
    // let params = { "section": section, "type": type, "portfolio": portfolioName};
    return await apiCalls.handleNewResponse(
        await apiCalls.api.post(
            `temperature/${value}`,
            JSON.stringify({
section, type, 
                portfolio,
            }),
            apiCalls.get_auth_header()
        )
    );

}

async function getAllTemperature(portfolio, section, type) {


    return await apiCalls.handleNewResponse(
        await apiCalls.api.get(
            `temperature/${portfolio}/${section}/${type}`,
       
                apiCalls.get_auth_header(),

        )
    );

}

async function getLastTemperature(portfolio, section, type) {


    return await apiCalls.handleNewResponse(
        await apiCalls.api.get(
            `temperature/${portfolio}/${section}/${type}/${"last"}`,
            apiCalls.get_auth_header()
            )
    );
}


export const apiTemperature = {
    addTemperature,
    getAllTemperature,
    getLastTemperature
    
    //
    //  deleteColour,
    // addColour,
    // getColourHistory
    // getAllColours,
    // getLastColour
}
