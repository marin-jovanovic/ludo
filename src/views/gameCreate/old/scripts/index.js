let c = 0;

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

            td.addEventListener('click', () => {
                if (td.innerText) {
                    console.log('delete')
                    td.innerText = ''
                    c--;
                } else {
                    td.innerText = c;
                    c++;
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

        let exportTable = [];

        let logSelected = {};


        for (let i = 0, row; row = table.rows[i]; i++) {

            exportTable[i] = [];

            let col;
            for (let j = 0; col = row.cells[j]; j++) {
                if (col.innerText) {

                    logSelected[col.innerText] = {
                        row: i,
                        column: j
                    };
                }
            }
        }

        console.table(logSelected)
        console.log(logSelected)



    })

}

function buildLayer() {

    let table = document.querySelector('table');

    for (var i = 0, row; row = table.rows[i]; i++) {


        for (var j = 0, col; col = row.cells[j]; j++) {
            col.addEventListener('click', i => {
                console.log(i.target)
                i.target.backgroundColor = 'black'

            })

        }
    }

}

window.onload = function() {
    tableCreate(15, 15);

    activateExportButton();

}

class BoardBuilder {
    constructor() {

    }
}

export const bb = {
    BoardBUilder,
}