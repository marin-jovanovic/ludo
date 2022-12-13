

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


    }

    addColumn = () => {

        let columnLength = Object.keys(this.board).length;
        let rowLength = Object.keys(this.board[0]).length;

        for (let i = 0; i < columnLength; i++) {
         
            this.board[i][rowLength] = this.defaultValue;

        }

    }

    selectLayer = ({layerId}) => {
        this.selectedLayer = layerId;
    }

    updateTile = ({row, column}) => {
        this.board[row][column] = String(this.selectLayer);
    }

    constructor({canvasElement}) {

        // todo
        this.selectedLayer = 1;

        this.canvas = canvasElement;

        this.canvas.width = innerWidth;
        this.canvas.height = innerHeight - 500;

        const ctx = this.canvas.getContext('2d');

        this.board = {
            0: {0: 0, 1: 1},
            1: {0: 2, 1: 3},
            
        };

        this.defaultValue = 0;
        
        this.addRow();

        this.addColumn();

        console.table(this.board)


        let wSize = 100;
        let hSize = 100;
      
        let height = Object.keys(this.board).length;

        let width = Object.keys(this.board[0]).length;


        for (let w = 0; w < width; w++) {
            for (let h = 0; h < height; h++) {

                ctx.fillStyle = ["red", "blue", "cyan", "yellow"][this.board[h][w]]

                // fillRect(x, y, width, height)
                ctx.fillRect(w * wSize, h * hSize, wSize, hSize);
            
            }
        }
        
        var elem = this.canvas;

        let elemLeft = elem.offsetLeft;
        let elemTop = elem.offsetTop;
        // let elements = [];

        // Add event listener for `click` events.
        elem.addEventListener('click', function(event) {
            var x = event.pageX - elemLeft,
                y = event.pageY - elemTop;
            // console.log(x, y);

            let xBlock = Math.floor(x / wSize);
            let yBlock = Math.floor(y / hSize);

            console.log("clicked", xBlock, yBlock)



            // for (let w = 0; w < width; w++) {
            //     for (let h = 0; h < height; h++) {

            //         // let element = 

            //         console.log()

            //         // if (
            //         //     y > element.top && 
            //         //     y < element.top + element.height && 
            //         //     x > element.left && 
            //         //     x < element.left + element.width
            //         // ) {
            //         //     console.log('clicked an element', w, h);
            //         // }
        
                
            //     }
            // }
    

            // elements.forEach(function(element) {
            //     if (y > element.top && y < element.top + element.height && x > element.left && x < element.left + element.width) {
            //         alert('clicked an element');
            //     }
            // });

        }, false);

    
    }

    // constructor({canvasElement}) {

    //     // todo
    //     this.selectedLayer = 1;

    //     this.canvas = canvasElement;

    //     this.canvas.width = innerWidth;
    //     this.canvas.height = innerHeight - 500;

    //     const ctx = this.canvas.getContext('2d');

    //     this.board = {
    //         0: {0: 0, 1: 1},
    //         1: {0: 2, 1: 3},
            
    //     };

    //     this.defaultValue = 0;
        
    //     this.addRow();

    //     this.addColumn();

    //     console.table(this.board)

    //     var tilesize = 30;

    //     // var map = {
    //     //     0: {0: 0, 1: 1},
    //     //     1: {0: 2, 1: 3},
    //     //     2: {0: 0, 1: 1},
    //     // }
      
    //     let height = Object.keys(this.board).length;

    //     let width = Object.keys(this.board[0]).length;


    //     for (let w = 0; w < width; w++) {
    //         for (let h = 0; h < height; h++) {

    //             ctx.fillStyle = ["red", "blue", "cyan", "yellow"][this.board[h][w]]

    //             ctx.fillRect(w * tilesize, h * tilesize, tilesize, tilesize)
            
    //         }
    //     }
        
    //     var elem = this.canvas;

    //     let elemLeft = elem.offsetLeft;
    //     let elemTop = elem.offsetTop;
    //     // let elements = [];

    //     // Add event listener for `click` events.
    //     elem.addEventListener('click', function(event) {
    //         var x = event.pageX - elemLeft,
    //             y = event.pageY - elemTop;
    //         console.log(x, y);

    //         for (let w = 0; w < width; w++) {
    //             for (let h = 0; h < height; h++) {

    //                 // let element = 

    //                 console.log()

    //                 // if (
    //                 //     y > element.top && 
    //                 //     y < element.top + element.height && 
    //                 //     x > element.left && 
    //                 //     x < element.left + element.width
    //                 // ) {
    //                 //     console.log('clicked an element', w, h);
    //                 // }
        
                
    //             }
    //         }
    

    //         // elements.forEach(function(element) {
    //         //     if (y > element.top && y < element.top + element.height && x > element.left && x < element.left + element.width) {
    //         //         alert('clicked an element');
    //         //     }
    //         // });

    //     }, false);




    //     // this.c = 0;

    //     // this.tableCreate(15, 15);
    
    //     // this.activateExportButton();
    
    // }

//     tableCreate = ({row, col}) => {
//         const body = document.body;
//         let tbl = document.createElement('table');

//         for (let i = 0; i < row; i++) {
//             const tr = tbl.insertRow();
//             for (let j = 0; j < col; j++) {

//                 const td = tr.insertCell();

//                 td.style.border = '1px solid black';
//                 td.style.backgroundColor = 'white'
//                 td.style.width = '20px'
//                 td.style.height = '20px'

//                 td.addEventListener('click', () => {
//                     if (td.innerText) {
//                         console.log('delete')
//                         td.innerText = ''
//                         this.c--;
//                     } else {
//                         td.innerText = this.c;
//                         this.c++;
//                     }
//                 })
//             }
//         }
//         body.appendChild(tbl);
//     }

//     activateExportButton = () => {
//     let exportButton = document.querySelector('#exportButton');

//     exportButton.addEventListener('click', () => {

//         let table = document.querySelector('table');

//         let exportTable = [];

//         let logSelected = {};

//         let row;
//         for (let i = 0; row = table.rows[i]; i++) {

//             exportTable[i] = [];

//             let col;
//             for (var j = 0; col = row.cells[j]; j++) {
//                 if (col.innerText) {
//                     logSelected[col.innerText] = { row: i, column: j };
//                 } 
//             }
//         }

//         console.table(logSelected)
//         console.log(logSelected)

//     })

// }

//     buildLayer = () => {

//     let table = document.querySelector('table');

//     for (var i = 0, row; row = table.rows[i]; i++) {


//         for (var j = 0, col; col = row.cells[j]; j++) {
//             // console.log(col)
//             col.addEventListener('click', i => {
//                 // console.log(i.target.style)
//                 console.log(i.target)
//                 // console.
//                 i.target.backgroundColor = 'black'
//                 // if (col.style.backgroundColor === 'black') {
//                 //     col.style.backgroundColor = 'white'
//                 // } else {
//                 //     col.style.backgroundColor = 'black'
//                 // }
//             })


//             // if (col.style.backgroundColor === 'black') {
//             //     exportTable[i][j] = selected
//             //     logSelected[logSelectedIndex] = { row: i, column: j };
//             //     logSelectedIndex++;
//             // } else {
//             //     exportTable[i][j] = unselected

//             // }
//         }
//     }

}


export const creator = {
    BoardBuilder
}
