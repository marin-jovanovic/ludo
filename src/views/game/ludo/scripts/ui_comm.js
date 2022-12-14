function remapPosition({i, j, Boundary}) {
    /**
     * for elements that are placed on tiles (ie. tokens)
     */

    return {
        x: j * Boundary.width + Boundary.width / 2,
        y: i * Boundary.height + Boundary.height / 2
    };

}

function remapTile({x,y, Boundary}) {
    /**
     * for tiles
     */

    return {
        x: Boundary.width * x,
        y: Boundary.height * y
    }
}


export { 
    remapPosition,
    remapTile
}