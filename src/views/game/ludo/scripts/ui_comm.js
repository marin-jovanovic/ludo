function remapPosition(i, j, Boundary) {
    return {
        x: j * Boundary.width + Boundary.width / 2,
        y: i * Boundary.height + Boundary.height / 2
    };

}

function remapTile({x,y, Boundary}) {
    return {
        x: Boundary.width * x,
        y: Boundary.height * y
    }
}


export { 
    remapPosition,
    remapTile
}