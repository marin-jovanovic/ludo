import { apiCalls } from './comm';

async function patchLocation(
    portfolioName,
    section,
    type
    
    , params) {

    return await apiCalls.handleNewResponse(
        await apiCalls.api.patch(
            `location/${portfolioName}/${section}/${type}`,
            {
                ...apiCalls.get_auth_header(),
                ...params

            }
        )
    );

}

async function deleteLocation(
    portfolioName,
name
    ) {
    // todo csrf

    return await apiCalls.handleNewResponse(
        await apiCalls.api.delete(
            `location/${portfolioName}/${name}`,
            apiCalls.get_auth_header()
        )
    );
}

async function addLocation(portfolio, name, section, type, latitude, longitude, csrfToken) {

    return await apiCalls.handleNewResponse(
        await apiCalls.api.post(
            // "location/",
            `location/${portfolio}/${name}`,
            JSON.stringify({
                portfolio,
                type, section, latitude, longitude, synchronizer_token: csrfToken
            }),
            apiCalls.get_auth_header()
        )
    );

}

async function getLocation(
    portfolioName,
    section,
    type
) {

    return await apiCalls.handleNewResponse(
        await apiCalls.api.get(
            `location/${portfolioName}/${section}/${type}`,
            apiCalls.get_auth_header()
        )
    );

}


async function getAllLocationsInPortfolio(
    portfolioName,
) {

    return await apiCalls.handleNewResponse(
        await apiCalls.api.get(
            `location/${portfolioName}`,
            apiCalls.get_auth_header()
        )
    );

}

export const apiLocation = {
    // deleteLocation,
    addLocation,
    getLocation,
    getAllLocationsInPortfolio,
    patchLocation,
    deleteLocation
}


// import { apiCalls } from './api';


// async function deleteLocation(i) {

//     const r = checkTokens()

//     if (r["status"]) {

//         let access_token = r["access_token"]
//         let refresh_token = r["refresh_token"]

//         const response = await apiCalls.api.post(`locations/`,
//             JSON.stringify({
//                 access_token,
//                 refresh_token,
//                 action: "locations;delete single",
//                 index: i
//             }));
//         return await apiCalls.handleNewResponse(response);

//     }

// }
// function checkTokens() {

//     if (sessionStorage.getItem("user") !== null) {
//         let user = JSON.parse(window.sessionStorage.getItem('user'));

//         if (
//             ("auth" in user) &&
//             ("access-token" in user["auth"]) &&
//             ("refresh-token" in user["auth"])
//         ) {

//             const access_token = user["auth"]["access-token"]
//             const refresh_token = user["auth"]["refresh-token"]

//             return {
//                 "status": true,
//                 "access_token": access_token,
//                 "refresh_token": refresh_token
//             }

//         }

//     }

//     return {
//         "status": false
//     }

// }

// async function addLocation(portfolio, section, type, latitude, longitude, csrfToken) {

//     return await apiCalls.handleNewResponse(
//         await apiCalls.api.post(
//             "locations/",
//             JSON.stringify({
//                 portfolio,
//                 type, section, latitude, longitude, synchronizer_token: csrfToken
//             }),
//             apiCalls.get_auth_header()
//         )
//     );


// }

// async function getLocationsFilterUsername(pn) {

//     return await apiCalls.handleNewResponse(
//         await apiCalls.api.get(
//             "locations/" + pn,
//             apiCalls.get_auth_header()
//         )
//     );

// }

// export const apiLocations = {
//     deleteLocation,
//     addLocation,
//     getLocationsFilterUsername
// }
