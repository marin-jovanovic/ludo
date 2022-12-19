
<template>
  <div v-for="i in this.types" :key="i">
    {{ i }}

    id:
    <input type="text" v-model="i.id" />

    colour:
    <input type="color" id="typeColor" v-model="i.colour" />
  </div>

  <select v-model="selected">
    <option v-for="item in this.types" v-bind:value="item" :key="item">
      {{ item.id }}
    </option>
  </select>

  <table ref="table"></table>

  row count:
  <input type="number" v-model="rowCount" @change="updateRowCount" />

  column count:
  <input type="number" v-model="columnCount" @change="updateColumnChange" />

  <table>
    <tr v-for="column in Object.entries(this.table)" :key="column[0]">
      <td
        :style="row[1].style"
        v-for="row in Object.entries(column[1])"
        :key="row[0]"
        @click="cellClicked(column[0], row[0])"
      >
        {{ row[1].value }}
      </td>
    </tr>
  </table>

  <button @click="exportTable">export</button>
</template>

<script>
export default {
  data() {
    return {
      boardBuilder: undefined,
      types: [
        { id: "1", colour: "" },
        { id: "2", colour: "" },
        { id: "3", colour: "" },
      ],
      selected: {},

      rowCount: 5,
      columnCount: 15,
      table: {},

      counter: 0,

      defaultColour: "white",
    };
  },
  mounted() {
    for (let r = 0; r < this.rowCount; r++) {
      let row = {};

      for (let c = 0; c < this.columnCount; c++) {
        row[c] = {
          style: {
            backgroundColor: "#16a085",
            border: "1px solid black",
            width: "40px",
            height: "40px",
          },
          value: undefined,
        };
      }

      this.table[r] = row;
    }

    this.table[2][2].type = "b";
  },
  methods: {
    getMaxKey(obj) {
      return Number(
        Object.keys(obj).reduce((a, b) => (obj[a] > obj[b] ? a : b))
      );
    },

    updateRowCount() {
      console.log("update row");

      let maxCount = this.getMaxKey(this.table);

      console.log(maxCount, this.rowCount);

      if (maxCount > this.rowCount) {
        let diff = this.rowCount - maxCount;
        console.log("rmeove", diff);

        for (let i = 0; i < diff; i++) {
          // const element = ];
          console.log("remove", maxCount + i);
          delete this.table[maxCount + i];
        }
      } else if (maxCount < this.rowCount) {
        let diff = this.rowCount - maxCount;
        console.log("add", diff);

        for (let i = 0; i < diff; i++) {
          let row = {};

          for (let c = 0; c < this.columnCount; c++) {
            row[c] = {
              style: {
                backgroundColor: "#16a085",
                border: "1px solid black",
                width: "40px",
                height: "40px",
              },
              value: undefined,
            };
          }

          this.table[maxCount + i] = row;
        }
      }

      // let maxCount =

      // for (const rowId of Object.keys(this.table)) {
      //   console.log(rowId);

      //   if (this.rowCount )
      // }
    },

    cellClicked(row, column) {
      if (!("colour" in this.selected)) {
        console.log("err: have to select sth");
        return;
      }

      let cell = this.table[row][column];

      if (cell.style.backgroundColor === this.selected.colour) {
        cell.style.backgroundColor = this.defaultColour;

        cell.value = undefined;

        this.counter--;
      } else {
        cell.style.backgroundColor = this.selected.colour;

        cell.value = this.counter;
        this.counter++;
      }
    },

    exportTable() {
      let logSelected = {};

      for (const [rowId, c] of Object.entries(this.table)) {
        for (const [columnId, meta] of Object.entries(c)) {
          if (meta.value || meta.value === 0) {
            logSelected[meta.value] = {
              row: rowId,
              column: columnId,
            };
          }
        }
      }

      console.table(logSelected);
      console.log(logSelected);
    },
  },
};
</script>

<style>
</style>