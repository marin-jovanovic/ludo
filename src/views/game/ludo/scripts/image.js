function createImage(src) {
    const image = new Image();
    image.src = src
    return image
}

export {
    createImage
}