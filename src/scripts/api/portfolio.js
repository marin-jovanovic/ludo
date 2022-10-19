import { apiCalls } from './comm';

async function createPortfolio(name, colour) {
    // todo csrf
    console.log("adding", name, colour)
    return await apiCalls.handleNewResponse(
        await apiCalls.api.post(
            `portfolio/${name}`,
            JSON.stringify({
                colour
            }),
            apiCalls.get_auth_header()
        )
    );
}

async function deletePortfolio(currentName) {
    // todo csrf

    return await apiCalls.handleNewResponse(
        await apiCalls.api.delete(
            "portfolio/" + currentName,
            apiCalls.get_auth_header()
        )
    );
}

async function getPortoflios() {

    return await apiCalls.handleNewResponse(
        await apiCalls.api.get(
            "portfolio/",
            apiCalls.get_auth_header()
        )
    );

}

async function patchPortoflios(portfolioOldName, params) {
    console.log(portfolioOldName, params)
 
    return await apiCalls.handleNewResponse(
        await apiCalls.api.patch(
            `portfolio/${portfolioOldName}`,
            {
                ...apiCalls.get_auth_header(),
                // "params": {
                //     params
                // }
                ...params

                // 'name': portfolioNewName,
                // "colour": portfolioNewColour
            }
        )
    );

}


export const apiPortfolio = {
    createPortfolio,
    deletePortfolio,
    getPortoflios,
    patchPortoflios
}