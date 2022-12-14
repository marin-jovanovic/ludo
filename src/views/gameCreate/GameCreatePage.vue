<!-- <template>
  <div>

    <div id="Div1" style=" float: left; width: 150px; overflow:scroll; ">
        <canvas id="boardBuilder" width="200" style="border:1px solid #ff0000;">
        
        </canvas>
    </div>

    <canvas id="boardBuilder" style="max-height: 1500px;max-width:1500px;overflow: scroll;">cant load canvas</canvas>

    <hr />
    row count
    <input type="number" @change="updateRow" v-model="rowCount" />

    <br />
    column count
    <input type="number" @change="updateColumn" v-model="columnCount" />

    <br />
    edit layer id
    <input type="number" @change="editLayer" v-model="layerId" />

   
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

    updateRow() {
      console.log("updateRow")
      this.boardBuilder.addRow();
    },
    updateColumn() {
      this.boardBuilder.addColumn();

    },

  },
};
</script> 

<style>
#boardBuilder {
  border-style: dotted;
}
</style> -->

<template>
  unselected:
  <input type="text" id="unselected" />

  selected:
  <input type="text" id="selected" />

  <table id="table"></table>

  <button id="exportButton">export</button>
</template>

<script>
import { bb } from "@/views/gameCreate/old/index.js";

export default {
  data() {
    return {
      boardBuilder: undefined,
    };
  },
  mounted() {
    this.boardBuilder = new bb.BoardBuilder({
      // body: document.body,
      table: document.querySelector("#table"),
      exportButton: document.querySelector("#exportButton"),
    });
  },
};
</script>

<style>
</style>