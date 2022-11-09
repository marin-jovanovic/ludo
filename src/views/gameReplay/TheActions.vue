<template>
    <div>
        <table>
            <tr v-for="(row, rowKey) in grid" :key="rowKey">
                <td v-for="(col, colKey) in row" :key="colKey" @click="selectCell(rowKey, colKey)"
                    :class="{ 'selected': cellSelected(rowKey, colKey) }">
                    <button>{{ col }}</button>
                </td>
            </tr>
        </table>
    </div>
</template>
    
    
<script>
import { apiGame } from "@/scripts/api/game";

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
            for (let i = 0; i <= 3; i++) {
                this.grid[i] = []
                for (let j = 0; j <= 3; j++) {
                    this.grid[i][j] = false
                }
            }
        },
        async selectCell(row, col) {
            // const newRow = this.grid[row].slice(0)
            // newRow[col] = true
            console.log('selected', row, col)
            this.username = sessionStorage.getItem("username");
            this.gameId = this.$route.params.id;

            console.log(this.username, this.gameId)

            let res = await apiGame.actionPerformed(
                this.gameId,
                this.username,
                "f"
                // this.instructionCurrentlyPerforming
            );

            if (!(res["auth"]["status"] && res["payload"]["status"])) {
                console.log("game leave err");
            }

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
