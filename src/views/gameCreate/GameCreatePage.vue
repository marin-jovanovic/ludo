
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
        { type: "1", colour: "#99c1f1" },
        { type: "2", colour: "#f9f06b" },
        { type: "3", colour: "#77767b" },
      ],
      selected: { type: "1", colour: "#99c1f1" },

      rowCount: 5,
      columnCount: 15,
      table: {},

      counter: 0,

      counterToCell: {},

      defaultColour: "#77767b",
    };
  },
  mounted() {
    this.clearTable();

    this.cellClicked(2, 1);
    this.cellClicked(3, 2);
    this.cellClicked(4, 3);
    this.cellClicked(3, 4);
    this.cellClicked(2, 5);
  },
  methods: {
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
};
</script>

<style>
</style>
