
<template>
  <BaseUserTemplate>
    <div v-for="i in this.types" :key="i">
      {{ i }}

      id:
      <input type="text" v-model="i.id" />

      colour:
      <input type="color" id="typeColor" v-model="i.colour" />
    </div>

    <select v-model="selected">
      <option v-for="item in this.types" v-bind:value="item" :key="item">
        {{ item.type }}
      </option>
    </select>

    <table ref="table"></table>

    row count:
    <input type="number" v-model="rowCount" @change="updateRowCount" />

    <br />

    column count:
    <input type="number" v-model="columnCount" @change="updateColumnChange" />

    <br />

    <button @click="clearTable">clear table</button>

    <br />
    <button @click="saveAsMap">save as map</button>

    <br />
    import
    <input type="text" v-model="imported" />
    <button @click="imp">import</button>

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
  </BaseUserTemplate>
</template>

<script>
import BaseUserTemplate from "@/components/BaseUserTemplate.vue";

export default {
  data() {
    return {
      imported: undefined,

      boardBuilder: undefined,
      types: [
        { type: "1", colour: "#99c1f1" },
        { type: "2", colour: "#f9f06b" },
        { type: "3", colour: "#77767b" },
      ],
      selected: { type: "1", colour: "#99c1f1" },

      rowCount: 15,
      columnCount: 15,
      table: {},

      counter: 0,

      counterToCell: {},

      defaultColour: "#77767b",
    };
  },
  mounted() {
    this.clearTable();

    // this.cellClicked(2, 1);
    // this.cellClicked(3, 2);
    // this.cellClicked(4, 3);
    // this.cellClicked(3, 4);
    // this.cellClicked(2, 5);
  },
  methods: {
    imp() {
      let b = {
        0: {
          row: "2",
          column: "11",
          type: "3",
        },
        1: {
          row: "3",
          column: "11",
          type: "3",
        },
        2: {
          row: "2",
          column: "12",
          type: "3",
        },
        3: {
          row: "3",
          column: "12",
          type: "3",
        },
        4: {
          row: "2",
          column: "2",
          type: "3",
        },
        5: {
          row: "3",
          column: "2",
          type: "3",
        },
        6: {
          row: "2",
          column: "3",
          type: "3",
        },
        7: {
          row: "3",
          column: "3",
          type: "3",
        },
        8: {
          row: "0",
          column: "6",
          type: "3",
        },
        9: {
          row: "2",
          column: "6",
          type: "3",
        },
        10: {
          row: "4",
          column: "6",
          type: "3",
        },
        11: {
          row: "5",
          column: "6",
          type: "3",
        },
        12: {
          row: "3",
          column: "6",
          type: "3",
        },
        13: {
          row: "1",
          column: "6",
          type: "3",
        },
        14: {
          row: "0",
          column: "8",
          type: "3",
        },
        15: {
          row: "1",
          column: "8",
          type: "3",
        },
        16: {
          row: "2",
          column: "8",
          type: "3",
        },
        17: {
          row: "3",
          column: "8",
          type: "3",
        },
        18: {
          row: "4",
          column: "8",
          type: "3",
        },
        19: {
          row: "5",
          column: "8",
          type: "3",
        },
        20: {
          row: "6",
          column: "9",
          type: "3",
        },
        21: {
          row: "6",
          column: "10",
          type: "3",
        },
        22: {
          row: "6",
          column: "11",
          type: "3",
        },
        23: {
          row: "6",
          column: "12",
          type: "3",
        },
        24: {
          row: "6",
          column: "13",
          type: "3",
        },
        25: {
          row: "6",
          column: "14",
          type: "3",
        },
        26: {
          row: "8",
          column: "14",
          type: "3",
        },
        27: {
          row: "8",
          column: "13",
          type: "3",
        },
        28: {
          row: "7",
          column: "14",
          type: "3",
        },
        29: {
          row: "8",
          column: "11",
          type: "3",
        },
        30: {
          row: "8",
          column: "10",
          type: "3",
        },
        31: {
          row: "8",
          column: "9",
          type: "3",
        },
        32: {
          row: "11",
          column: "11",
          type: "3",
        },
        33: {
          row: "12",
          column: "11",
          type: "3",
        },
        34: {
          row: "11",
          column: "12",
          type: "3",
        },
        35: {
          row: "12",
          column: "12",
          type: "3",
        },
        36: {
          row: "11",
          column: "2",
          type: "3",
        },
        37: {
          row: "12",
          column: "2",
          type: "3",
        },
        38: {
          row: "11",
          column: "3",
          type: "3",
        },
        39: {
          row: "12",
          column: "3",
          type: "3",
        },
        40: {
          row: "6",
          column: "0",
          type: "3",
        },
        41: {
          row: "6",
          column: "1",
          type: "3",
        },
        42: {
          row: "6",
          column: "2",
          type: "3",
        },
        43: {
          row: "6",
          column: "4",
          type: "3",
        },
        44: {
          row: "6",
          column: "5",
          type: "3",
        },
        45: {
          row: "6",
          column: "3",
          type: "3",
        },
        46: {
          row: "8",
          column: "0",
          type: "3",
        },
        47: {
          row: "8",
          column: "1",
          type: "3",
        },
        48: {
          row: "8",
          column: "3",
          type: "3",
        },
        49: {
          row: "8",
          column: "4",
          type: "3",
        },
        50: {
          row: "8",
          column: "5",
          type: "3",
        },
        51: {
          row: "9",
          column: "6",
          type: "3",
        },
        52: {
          row: "10",
          column: "6",
          type: "3",
        },
        53: {
          row: "11",
          column: "6",
          type: "3",
        },
        54: {
          row: "12",
          column: "6",
          type: "3",
        },
        55: {
          row: "13",
          column: "6",
          type: "3",
        },
        56: {
          row: "14",
          column: "6",
          type: "3",
        },
        57: {
          row: "9",
          column: "8",
          type: "3",
        },
        58: {
          row: "10",
          column: "8",
          type: "3",
        },
        59: {
          row: "12",
          column: "8",
          type: "3",
        },
        60: {
          row: "13",
          column: "8",
          type: "3",
        },
        61: {
          row: "14",
          column: "7",
          type: "3",
        },
        62: {
          row: "14",
          column: "8",
          type: "3",
        },
        63: {
          row: "11",
          column: "8",
          type: "3",
        },
        64: {
          row: "8",
          column: "2",
          type: "3",
        },
        65: {
          row: "7",
          column: "0",
          type: "3",
        },
        66: {
          row: "7",
          column: "1",
          type: "3",
        },
        67: {
          row: "7",
          column: "2",
          type: "3",
        },
        68: {
          row: "7",
          column: "3",
          type: "3",
        },
        69: {
          row: "7",
          column: "4",
          type: "3",
        },
        70: {
          row: "7",
          column: "5",
          type: "3",
        },
        71: {
          row: "7",
          column: "6",
          type: "3",
        },
        72: {
          row: "6",
          column: "7",
          type: "3",
        },
        73: {
          row: "5",
          column: "7",
          type: "3",
        },
        74: {
          row: "4",
          column: "7",
          type: "3",
        },
        75: {
          row: "3",
          column: "7",
          type: "3",
        },
        76: {
          row: "2",
          column: "7",
          type: "3",
        },
        77: {
          row: "1",
          column: "7",
          type: "3",
        },
        78: {
          row: "0",
          column: "7",
          type: "3",
        },
        79: {
          row: "7",
          column: "8",
          type: "3",
        },
        80: {
          row: "7",
          column: "9",
          type: "3",
        },
        81: {
          row: "7",
          column: "10",
          type: "3",
        },
        82: {
          row: "7",
          column: "11",
          type: "3",
        },
        83: {
          row: "7",
          column: "12",
          type: "3",
        },
        84: {
          row: "7",
          column: "13",
          type: "3",
        },
        85: {
          row: "8",
          column: "7",
          type: "3",
        },
        86: {
          row: "9",
          column: "7",
          type: "3",
        },
        87: {
          row: "10",
          column: "7",
          type: "3",
        },
        88: {
          row: "11",
          column: "7",
          type: "3",
        },
        89: {
          row: "12",
          column: "7",
          type: "3",
        },
        90: {
          row: "13",
          column: "7",
          type: "3",
        },
        91: {
          row: "8",
          column: "12",
          type: "3",
        },
      };

      // console.log(b);

      //         0: {
      // row: "2",
      //   column: "11",
      //   type: "3",
      // },

      this.selected = { type: "3", colour: "#77767b" };

      for (const f of Object.values(b)) {
        // console.log(f, Number(f.row), Number(f.column));

        this.cellClicked(Number(f.row), Number(f.column));
      }

      console.log(this.imported);
      // load;

      // this.imported =
      //   '[{"row": "7", "col": "6", "p": "0", "t": "0"}, {"row": "7", "col": "5", "p": "0", "t": "1"}, {"row": "7", "col": "4", "p": "0", "t": "2"}, {"row": "8", "col": "12", "p": "0", "t": "3"}, {"row": "6", "col": "7", "p": "1", "t": "0"}, {"row": "5", "col": "7", "p": "1", "t": "1"}, {"row": "4", "col": "7", "p": "1", "t": "2"}, {"row": "0", "col": "7", "p": "1", "t": "3"} ]';

      // this.imported =

      let parsed = JSON.parse(this.imported);
      console.log(parsed);

      parsed.forEach((i) => {
        // console.log(i);

        if (i.p === "0") {
          this.selected = { type: "1", colour: "#99c1f1" };
        } else {
          this.selected = { type: "2", colour: "#f9f06b" };
        }

        this.cellClicked(i.row, i.col);
        this.cellClicked(i.row, i.col);
      });
    },

    saveAsMap() {
      this.exportTable();
    },

    clearTable() {
      for (let r = 0; r < this.rowCount; r++) {
        let row = {};

        for (let c = 0; c < this.columnCount; c++) {
          row[c] = this.getNewTile();
        }

        this.table[r] = row;
      }

      this.counter = 0;
      this.counterToCell = {};
    },

    // comm
    getMaxKey(obj) {
      return Number(
        Object.keys(obj).reduce((a, b) => (obj[a] > obj[b] ? a : b))
      );
    },

    arraySortNumbers(arr) {
      arr.sort(function (a, b) {
        return a - b;
      });
    },

    isCellSelected(row, column) {
      let meta = this.table[row][column];

      if (!("value" in meta)) {
        console.log("err no value");
        console.log(meta.value);
      }

      if (meta.value === 0) {
        return true;
      }

      return !isNaN(meta.value);
    },

    updateColumnChange() {
      /**
       * read update row change for docs
       */

      let firstRowId = 0;
      let currentNumberOfColumns = this.getMaxKey(this.table[firstRowId]) + 1;

      if (currentNumberOfColumns > this.columnCount) {
        let numberOfColumnsToRemove = currentNumberOfColumns - this.columnCount;

        console.log("remove", numberOfColumnsToRemove);

        let removedTiles = [];

        for (let i = 0; i < numberOfColumnsToRemove; i++) {
          for (const row of Object.keys(this.table)) {
            let tile = this.table[row][currentNumberOfColumns + i - 1];

            if (this.isCellSelected(row, currentNumberOfColumns + i - 1)) {
              removedTiles.push(tile);
            }

            // // this will cause err in consistency
            delete this.table[row][currentNumberOfColumns + i - 1];
          }
        }

        let removedTilesIndexes = removedTiles.map((i) => i.value);

        console.log("removed tile indexes", removedTilesIndexes);

        this.arraySortNumbers(removedTilesIndexes);

        while (removedTilesIndexes?.length) {
          let index = removedTilesIndexes.pop(0);

          this.removeIndex(index);
        }
      } else if (currentNumberOfColumns < this.columnCount) {
        let numberOfColumnsToAdd = this.columnCount - currentNumberOfColumns;

        for (let i = 0; i < numberOfColumnsToAdd; i++) {
          for (const row of Object.keys(this.table)) {
            this.table[row][currentNumberOfColumns + i] = this.getNewTile();
          }
        }
      }

      console.log("update column count");
      this.checkBoardConsistent();
    },

    updateRowCount() {
      /**
       * this presents new err
       *
       * if we have
       * / 1 /
       * / 3 4
       * / 5 2
       *
       * and remove last row
       * then we aim to get this
       * / 1 /
       * / 2 3
       * - - -
       *
       * or
       *
       * / 1 /
       * / 3 4
       * - - -
       *
       * and c is 2, and after 2 we go to 5
       *
       * i like first option
       *
       * deleted is {5, 2}
       * max count is 5
       * {1, 2, 3, 4, 5} -> {1, 3, 4} -> {1, 2, 3}
       * update those 3 numbers
       *
       * case delete {1, 2}
       * {1, 2, 3, 4, 5} -> {3, 4, 5} -> {1, 2, 3}
       *
       */

      let currentNumberOfRows = this.getMaxKey(this.table) + 1;

      if (currentNumberOfRows > this.rowCount) {
        let numberOfRowsToRemove = currentNumberOfRows - this.rowCount;

        let removedTiles = [];

        for (let i = 0; i < numberOfRowsToRemove; i++) {
          let rowScheduledForRemoving = currentNumberOfRows - 1 - i;

          for (const [columnId, tile] of Object.entries(
            this.table[rowScheduledForRemoving]
          )) {
            if (this.isCellSelected(rowScheduledForRemoving, columnId)) {
              removedTiles.push(tile);
            }
          }

          // this will cause err in check consistency
          delete this.table[rowScheduledForRemoving];
        }

        let removedTilesIndexes = removedTiles.map((i) => i.value);

        console.log("removed tile indexes", removedTilesIndexes);

        /**
         *
         *   x     x
         * 1 2 3 4 5 6 7
         *
         * shift (6, 7) x 2
         * shift (3, 4) x 1
         *
         *     x
         * 0 1 2
         *
         *
         */

        this.arraySortNumbers(removedTilesIndexes);

        while (removedTilesIndexes?.length) {
          let index = removedTilesIndexes.pop(0);
          this.removeIndex(index);
        }
      } else if (currentNumberOfRows < this.rowCount) {
        let diff = this.rowCount - currentNumberOfRows;
        console.log("add", diff);

        for (let i = 0; i < diff; i++) {
          let row = {};

          for (let c = 0; c < this.columnCount; c++) {
            row[c] = this.getNewTile();
          }

          this.table[currentNumberOfRows + i] = row;
        }
      }
      console.log("update row count");
      this.checkBoardConsistent();
    },
    checkBoardConsistent() {
      let tileVals = [];

      // console.log("check");

      // let ctcCheck = Object.keys(this.counterToCell);
      // console.log("ctc keys", ctcCheck);

      // // console.log("counter to cell");
      // for (const [counter, cell] of Object.entries(this.counterToCell)) {
      //   if (Number(counter) !== cell.value) {
      //     console.log("err", counter, cell.value);
      //   }

      //   // console.log(counter, cell);
      // }

      // console.log("board");
      // for (let r = 0; r < this.rowCount; r++) {
      //   for (let c = 0; c < this.columnCount; c++) {
      //     if (this.isCellSelected(r, c)) {
      //       console.log(this.table[r][c].value);
      //     }
      //   }
      // }

      for (let r = 0; r < this.rowCount; r++) {
        for (let c = 0; c < this.columnCount; c++) {
          let v = this.table[r][c].value;

          if (this.isCellSelected(r, c) !== (v === 0 || Boolean(v))) {
            console.log(
              "err mismatch",
              r,
              c,
              this.isCellSelected(r, c),
              Boolean(v),
              v
            );
          }

          if (this.isCellSelected(r, c)) {
            let tileValue = this.table[r][c].value;

            tileVals.push(tileValue);
          }
        }
      }

      let allGood = true;

      this.arraySortNumbers(tileVals);

      for (let i = 0; i < tileVals.length; i++) {
        if (!tileVals.includes(i)) {
          console.log("err missing", i);
          console.log("what i have", tileVals);
          allGood = false;
        }
      }

      console.log("consistency check", allGood);
    },

    getNewTile() {
      return {
        style: {
          backgroundColor: "#16a085",
          border: "1px solid black",
          width: "40px",
          height: "40px",
        },
        value: undefined,
        type: undefined,
      };
    },

    renameObjectKey(o, oldKey, newKey) {
      if (oldKey !== newKey && o[oldKey] && !o[newKey]) {
        Object.defineProperty(
          o,
          newKey,
          Object.getOwnPropertyDescriptor(o, oldKey)
        );

        delete o[oldKey];
      }
    },

    removeIndex(index) {
      /**
       * remove cell at index
       * shift all higher indexes
       * set counter to max count
       *
       */

      console.log("remove", index);
      delete this.counterToCell[index];

      let scheduledForDecrementing = [];

      for (const [counter, cell] of Object.entries(this.counterToCell)) {
        if (Number(counter) !== cell.value) {
          console.log("err", counter, cell.value);
        }

        if (Number(counter) > index) {
          scheduledForDecrementing.push(cell);
        }
      }

      scheduledForDecrementing.forEach((i) => {
        let oldKey = i.value;
        let newKey = i.value - 1;

        i.value -= 1;

        this.renameObjectKey(
          this.counterToCell,
          Number(oldKey),
          Number(newKey)
        );
      });

      if (Object.keys(this.counterToCell)?.length) {
        this.counter = this.getMaxKey(this.counterToCell) + 1;
      } else {
        this.counter = 0;
      }

      console.log("next tile will have value:", this.counter);

      this.checkBoardConsistent();
    },

    cellClicked(row, column) {
      if (!("colour" in this.selected)) {
        console.log("err: have to select sth");
        return;
      }

      let cell = this.table[row][column];

      if (this.isCellSelected(row, column)) {
        cell.style.backgroundColor = this.defaultColour;

        let tileValue = cell.value;
        cell.value = undefined;
        cell.type = undefined;

        this.removeIndex(tileValue);
      } else {
        cell.style.backgroundColor = this.selected.colour;

        this.counterToCell[this.counter] = cell;

        cell.value = this.counter;
        cell.type = this.selected.type;
        this.counter++;
      }

      this.checkBoardConsistent();
    },

    exportTable() {
      let logSelected = {};

      for (const [rowId, c] of Object.entries(this.table)) {
        for (const [columnId, meta] of Object.entries(c)) {
          if (meta.value || meta.value === 0) {
            logSelected[meta.value] = {
              row: rowId,
              column: columnId,
              type: meta.type,
            };
          }
        }
      }

      console.table(logSelected);
      console.log(logSelected);
    },
  },
  components: {
    BaseUserTemplate,
  },
};
</script>

<style>
</style>
