class BoardBuilder {
    constructor({
        table,
        exportButton
    }) {

        this.table = table;
        this.exportButton = exportButton;

        this.c = 0;

        this.tableCreate(15, 15);

        this.activateExportButton();
    }


    tableCreate = (row, col) => {

        for (let i = 0; i < row; i++) {
            const tr = this.table.insertRow();
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
                        this.c--;
                    } else {
                        td.innerText = this.c;
                        this.c++;
                    }
                })
            }
        }
    }

    activateExportButton = () => {

        this.exportButton.addEventListener('click', () => {

            let exportTable = [];
            let logSelected = {};

            for (let i = 0; i < this.table.rows.length; i++) {
                let row = this.table.rows[i];

                exportTable[i] = [];

                for (let j = 0; j < row.cells.length; j++) {
                    let col = row.cells[j];
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
}

export const bb = {
    BoardBuilder,
}