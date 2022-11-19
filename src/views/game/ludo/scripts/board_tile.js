class BoardTile {
    static width = 40;
    static height = 40;

    constructor({ position, image }) {
        this.position = position;
        // this.width = 40;
        // this.height = 40;
        this.image = image
    }

    draw(canvas) {

        canvas.drawImage(this.image, this.position.x, this.position.y)

    }

}

export { BoardTile }