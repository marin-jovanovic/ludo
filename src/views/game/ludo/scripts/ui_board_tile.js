class BoardTile {

    static width = 40;
    static height = 40;

    constructor({ position, image }) {


        this.position = position;
        this.image = image;
    }

    draw(canvas) {

        let image = this.image
        let position = this.position;

        this.image.onload = () => {
            canvas.drawImage(image, position.x, position.y)

        }

        // this.image.onload = () => {
        //     canvas.drawImage(this.image, this.position.x, this.position.y)

        // }; 


// function drawImageActualSize() {
//     canvas.drawImage(this.image, this.position.x, this.position.y)
//   }

        // canvas.drawImage(this.image, this.position.x, this.position.y)

    }

}

export { BoardTile }