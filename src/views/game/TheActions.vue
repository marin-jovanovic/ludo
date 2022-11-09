<template>
    <div>
        <table>

            <div>
                <div v-for="r in 4" :key="r">

                    <button @click="move(r, t)" v-for="t in 4" :key="t">
                        token {{ t }}
                    </button>
                </div>

                <!-- <button>1</button> -->
            </div>

            <!-- <tr v-for="(row, rowKey) in grid" :key="rowKey">
                <td v-for="(col, colKey) in row" :key="colKey" @click="selectCell(rowKey, colKey)"
                    :class="{ 'selected': cellSelected(rowKey, colKey) }">
                    <button>{{ col }}</button>
                </td>
            </tr> -->
        </table>
    </div>
</template>
    
    
<script>
import { apiGame } from "@/scripts/api/game";

export default {
    created() {
    },
    data() {
        return {
        }
    },
    methods: {
        async move(player, token) {
            console.log(player, token)


            this.username = sessionStorage.getItem("username");
            this.gameId = this.$route.params.id;

            // todo pair username with col

            let res = await apiGame.actionPerformed(
                this.gameId,
                this.username,
                String(token)
            );

            if (!(res["auth"]["status"] && res["payload"]["status"])) {
                console.log("action perfromred err");
            }

        },
    }
}

</script> 
