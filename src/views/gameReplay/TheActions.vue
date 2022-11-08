<template>
    <div>
        <table>
            <tr v-for="(row, rowKey) in grid" :key="rowKey">
                <th class="row-col-label">{{ rowKey + 1 }}</th>
                <td v-for="(col, colKey) in row" :key="colKey" @click="selectCell(rowKey, colKey)"
                    :class="{ 'selected': cellSelected(rowKey, colKey) }">
                    {{ col }}
                </td>
            </tr>
        </table>
    </div>
</template>
    
    
<script>

export default {
    created() {
        this.initColHead()
        this.createSpreadSheet()
    },
    data() {
        return {
            selected: '',
            grid: [],
            colHead: [' '],
            isSelected: false
        }
    },
    methods: {
        initColHead() {
            this.colHead.push(...'ABC'.split(''))
        },
        createSpreadSheet() {
            for (let i = 0; i <= 2; i++) {
                this.grid[i] = []
                for (let j = 0; j <= 2; j++) {
                    this.grid[i][j] = false
                }
            }
        },
        selectCell(row, col) {
            const newRow = this.grid[row].slice(0)
            newRow[col] = true
            console.log('selected', row, col)
        },
        cellSelected(row, col) {
            return (this.grid[row][col] === true)
        }
    }
}

// export default {
//     data() {
//         return {};
//     },
//     mounted() {
//     },
//     methods: {

//     },
// };
</script> 
