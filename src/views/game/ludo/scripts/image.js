function createImage({source}) {
    const image = new Image();
    image.src = source

    return image
}

export {
    createImage
}