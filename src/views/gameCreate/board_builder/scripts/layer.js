function tableCreate(row, col) {
    const body = document.body;
    let tbl = document.createElement('table');

    for (let i = 0; i < row; i++) {
        const tr = tbl.insertRow();
        for (let j = 0; j < col; j++) {

            const td = tr.insertCell();

            td.style.border = '1px solid black';
            td.style.backgroundColor = 'white'
            td.style.width = '20px'
            td.style.height = '20px'

            td.addEventListener('click', i => {

                if (td.style.backgroundColor === 'black') {
                    td.style.backgroundColor = 'white'
                } else {
                    td.style.backgroundColor = 'black'
                }

            })
        }
    }
    body.appendChild(tbl);
}

function activateExportButton() {
    let exportButton = document.querySelector('#exportButton');

    exportButton.addEventListener('click', i => {

        let table = document.querySelector('table');

        let selected = document.querySelector('#selected').value;
        let unselected = document.querySelector('#unselected').value;

        let exportTable = [];

        let logSelected = {};
        let logSelectedIndex = 0;


        for (var i = 0, row; row = table.rows[i]; i++) {

            exportTable[i] = [];

            for (var j = 0, col; col = row.cells[j]; j++) {
                if (col.style.backgroundColor === 'black') {
                    exportTable[i][j] = selected
                    logSelected[logSelectedIndex] = { row: i, column: j };
                    logSelectedIndex++;
                } else {
                    exportTable[i][j] = unselected

                }
            }
        }

        console.table(exportTable)

        console.log(exportTable)
        console.table(logSelected)
        console.log(logSelected)



    })

}

function buildLayer() {

    let table = document.querySelector('table');

    for (var i = 0, row; row = table.rows[i]; i++) {


        for (var j = 0, col; col = row.cells[j]; j++) {
            // console.log(col)
            col.addEventListener('click', i => {
                // console.log(i.target.style)
                console.log(i.target)
                // console.
                i.target.backgroundColor = 'black'
                // if (col.style.backgroundColor === 'black') {
                //     col.style.backgroundColor = 'white'
                // } else {
                //     col.style.backgroundColor = 'black'
                // }
            })


            // if (col.style.backgroundColor === 'black') {
            //     exportTable[i][j] = selected
            //     logSelected[logSelectedIndex] = { row: i, column: j };
            //     logSelectedIndex++;
            // } else {
            //     exportTable[i][j] = unselected

            // }
        }
    }

}

window.onload = function () {
    tableCreate(15, 15);

    activateExportButton();

}
