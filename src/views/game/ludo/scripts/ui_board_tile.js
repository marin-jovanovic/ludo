class BoardTile {

    static width = 40;
    static height = 40;

    constructor({ position, image }) {
        this.position = position;
        this.image = image;
    }

    draw(canvas) {

        this.image.onload = () => {
            canvas.drawImage(
                this.image, 
                this.position.x, 
                this.position.y
            );
        }

    }

}

export { BoardTile }