/**
 * todo
 * 
 * scrolling?
 * layers
 * export
 */

// function run () => {
//     window.onload = function () {

//     }


// }

class BoardBuilder {

    /**
     * todo delete row & column
     */


    addRow = () => {


        let columnLength = Object.keys(this.board).length;

        let rowLength = Object.keys(this.board[0]).length;

        this.board[columnLength] = {}

        for (let i = 0; i < rowLength; i++) {

            this.board[columnLength][i] = this.defaultValue;

        }

        this.redraw();

    }

    addColumn = () => {

        let columnLength = Object.keys(this.board).length;
        let rowLength = Object.keys(this.board[0]).length;

        for (let i = 0; i < columnLength; i++) {

            this.board[i][rowLength] = this.defaultValue;

        }

        this.redraw();
    }

    selectLayer = ({
        layerId
    }) => {
        this.selectedLayer = layerId;

    }

    updateTile = ({
        row,
        column
    }) => {
        this.board[row][column] = String(this.selectLayer);

    }

    // draw a single rect
    rect = (x, y, w, h) => {
        this.ctx.beginPath();
        this.ctx.rect(x, y, w, h);
        this.ctx.closePath();
        this.ctx.fill();
    }

    // clear the canvas
    clear = () => {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    }

    // redraw the scene
    draw = () => {
        this.clear();
        this.ctx.fillStyle = "#FAF7F8";
        this.rect(0, 0, this.canvas.width, this.canvas.height);
        // redraw each rect in the rects[] array
        for (var i = 0; i < this.rects.length; i++) {
            var r = this.rects[i];
            this.ctx.fillStyle = r.fill;
            this.rect(r.x, r.y, r.width, r.height);
        }
    }

    // handle mousedown events
    myDown = (e) => {

        // tell the browser we're handling this mouse event
        e.preventDefault();
        e.stopPropagation();

        // get the current mouse position
        var mx = parseInt(e.clientX - this.offsetX);
        var my = parseInt(e.clientY - this.offsetY);

        // test each rect to see if mouse is inside
        this.dragok = false;
        for (var i = 0; i < this.rects.length; i++) {
            var r = this.rects[i];
            if (mx > r.x && mx < r.x + r.width && my > r.y && my < r.y + r.height) {
                // if yes, set that rects isDragging=true
                this.dragok = true;
                r.isDragging = true;
            }
        }
        // save the current mouse position
        this.startX = mx;
        this.startY = my;
    }


    // handle mouseup events
    myUp = (e) => {
        // tell the browser we're handling this mouse event
        e.preventDefault();
        e.stopPropagation();

        // clear all the dragging flags
        this.dragok = false;
        for (var i = 0; i < this.rects.length; i++) {
            this.rects[i].isDragging = false;
        }
    }


    // handle mouse moves
    myMove = (e) => {
        if (this.dragok) {

            e.preventDefault();
            e.stopPropagation();

            var mx = parseInt(e.clientX - this.offsetX);
            var my = parseInt(e.clientY - this.offsetY);


            var dx = mx - this.startX;
            var dy = my - this.startY;

            // move each rect that isDragging 
            // by the distance the mouse has moved
            // since the last mousemove
            for (var i = 0; i < this.rects.length; i++) {
                var r = this.rects[i];
                if (r.isDragging) {
                    r.x += dx;
                    r.y += dy;
                }
            }

            // redraw the scene with the new rect positions
            this.draw();

            // reset the starting mouse position for the next mousemove
            this.startX = mx;
            this.startY = my;

        }
    }

    redraw = () => {

        let height = Object.keys(this.board).length;

        let width = Object.keys(this.board[0]).length;

        console.log(width)

        for (let w = 0; w < width; w++) {
            for (let h = 0; h < height; h++) {

                this.ctx.fillStyle = ["red", "blue", "cyan", "yellow"][this.board[h][w]]

                // fillRect(x, y, width, height)
                this.ctx.fillRect(w * this.wSize, h * this.hSize, this.wSize, this.hSize);

            }
        }

    }

    constructor({
        canvasElement
    }) {

        // todo
        this.selectedLayer = 1;

        this.canvas = canvasElement;

        this.canvas.width = innerWidth;
        this.canvas.height = innerHeight - 500;

        this.ctx = this.canvas.getContext('2d');

        this.board = {
            0: {
                0: 0,
                1: 1
            },
            1: {
                0: 2,
                1: 3
            },

        };

        this.defaultValue = 0;

        this.addRow();

        this.addColumn();

        console.table(this.board)


        this.wSize = 100;
        this.hSize = 100;

        this.redraw();

        /**
         * drag and drop part
         */


        // // get canvas related references
        // var BB = this.canvas.getBoundingClientRect();
        // this.offsetX = BB.left;
        // this.offsetY = BB.top;
        // // var WIDTH = this.canvas.width;
        // // var HEIGHT = this.canvas.height;

        // // drag related variables
        // this.dragok = false;
        // this.startX;
        // this.startY;

        // // an array of objects that define different rectangles
        // this.rects = [];
        // this.rects.push({
        //     x: 75 - 15,
        //     y: 50 - 15,
        //     width: 30,
        //     height: 30,
        //     fill: "#444444",
        //     isDragging: false
        // });
        // this.rects.push({
        //     x: 75 - 25,
        //     y: 50 - 25,
        //     width: 30,
        //     height: 30,
        //     fill: "#ff550d",
        //     isDragging: false
        // });
        // this.rects.push({
        //     x: 75 - 35,
        //     y: 50 - 35,
        //     width: 30,
        //     height: 30,
        //     fill: "#800080",
        //     isDragging: false
        // });
        // this.rects.push({
        //     x: 75 - 45,
        //     y: 50 - 45,
        //     width: 30,
        //     height: 30,
        //     fill: "#0c64e8",
        //     isDragging: false
        // });

        // // listen for mouse events
        // this.canvas.onmousedown = this.myDown;
        // this.canvas.onmouseup = this.myUp;
        // this.canvas.onmousemove = this.myMove;

        // // call to draw the scene
        // this.draw();

        /**
         * 
         */




        /**
         * this will colour curr block to black
         */

        let elemLeft = this.canvas.offsetLeft;
        let elemTop = this.canvas.offsetTop;

        this.canvas.addEventListener('click', (event) => {
            var x = event.pageX - elemLeft,
                y = event.pageY - elemTop;
            // console.log(x, y);

            let xBlock = Math.floor(x / this.wSize);
            let yBlock = Math.floor(y / this.hSize);

            console.log("clicked", xBlock, yBlock);

            this.board[yBlock][xBlock] = -1;
            this.ctx.fillStyle = "black";
            this.ctx.fillRect(xBlock * this.wSize, yBlock * this.hSize, this.wSize, this.hSize);


        }, false);


    }

}


export const creator = {
    BoardBuilder
}