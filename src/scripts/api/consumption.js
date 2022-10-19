import { apiCalls } from './comm';

async function addConsumption(portfolio, section, type, value) {
    // let params = { "section": section, "type": type, "portfolio": portfolioName};
    return await apiCalls.handleNewResponse(
        await apiCalls.api.post(
            `consumption/${value}`,
            JSON.stringify({
section, type, 
                portfolio,
            }),
            apiCalls.get_auth_header()
        )
    );

}

async function getAllConsumption(portfolio, section, type) {


    return await apiCalls.handleNewResponse(
        await apiCalls.api.get(
            `consumption/${portfolio}/${section}/${type}`,
       
                apiCalls.get_auth_header(),

        )
    );

}

async function getLastConsumption(portfolio, section, type) {


    return await apiCalls.handleNewResponse(
        await apiCalls.api.get(
            `consumption/${portfolio}/${section}/${type}/${"last"}`,
            apiCalls.get_auth_header()
            )
    );
}


export const apiConsumption = {
    addConsumption,
    getAllConsumption,
    getLastConsumption,
    // addTemperature,
    // getAllTemperature,
    // getLastTemperature
    
    //
    //  deleteColour,
    // addColour,
    // getColourHistory
    // getAllColours,
    // getLastColour
}
