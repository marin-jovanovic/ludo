
class Canvas {
    constructor(element) {
        this.canvas = element;
        this.canvas.width = 600;
        this.canvas.height = 600;
        // this.canvas.width = innerWidth;
        // this.canvas.height = innerHeight;

        this.context = this.canvas.getContext("2d");

        this.animationId;
    }

    clear = () => {

        // leave no trace
        this.context.clearRect(0, 0, this.canvas.width, this.canvas.height)

    }




}


// class CanvasGame extends Canvas {
 
// }


export { 
    Canvas
    // CanvasGame 
}