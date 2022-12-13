<template>
  <div>
    <canvas id="boardBuilder">cant load canvas</canvas>

    <hr />
    row count
    <input type="number" @change="updateBoard" v-model="rowCount" />

    <br />
    column count
    <input type="number" @change="updateBoard" v-model="columnCount" />

    <br />
    edit layer id
    <input type="number" @change="editLayer" v-model="layerId" />

    <!-- <button @click="addRow">add column</button>
    <button @click="addColumn">remove row</button> -->

    <!-- unselected:
    <input type="text" id="unselected" />

    selected:
    <input type="text" id="selected" />

    <button id="exportButton">export</button> -->

    <!-- <button>add row</button>
    <button>add column</button>
    <button>remove row</button>
    <button>remove column</button> -->
    <!-- <table></table> -->
  </div>
</template>


<script>
import { creator } from "@/views/gameCreate/board_builder/scripts/index.js";

export default {
  data() {
    return {
      rowCount: 10,
      columnCount: 5,
      layerId: 1,
    };
  },
  mounted() {
    this.boardBuilder = new creator.BoardBuilder({
      canvasElement: document.querySelector("#boardBuilder"),
    });
  },
  methods: {
    editLayer() {
      this.boardBuilder.selectLayer({
        layerId: this.layerId,
      });
    },

    updateBoard() {
      console.log("update");
    },
  },
};
</script> 

<style>
#boardBuilder {
  border-style: dotted;
}
</style>

