<template>
  <div :style="this.diceStyle" id="dice" @click="rollDice(5)">
    <div
      v-for="(a, b) in this.config"
      :key="b"
      class="side"
      :id="b"
      :style="this.style[b]"
    >
      <div
        v-for="(d, k) in a.dots"
        :key="k"
        class="dot"
        :class="d"
        :style="this.style[d]"
      ></div>
    </div>
  </div>
</template>
  

<style>
#dice {
  width: 100px;
  height: 100px;
  transform-style: preserve-3d;
  transition: transform 1s;
  /* position: absolute; */
  /* left: 150px; */
}

.dot {
  position: absolute;
  width: 20px;
  height: 20px;
  margin: -10px 5px 5px -10px;
  border-radius: 20px;
  background-color: white;
}

.side {
  position: absolute;
  background-color: black;
  border-radius: 5px;
  width: 100px;
  height: 100px;
  line-height: 2em;
}
</style>
  
<script>
export default {
  data() {
    return {
      value: -1,
      diceElement: undefined,
      currX: 0,
      currY: 0,

      config: {
        one: {
          dots: ["center-center"],
          rotations: {
            x: 0,
            y: 0,
          },
          initRotation: {
            x: 0,
            y: 0,
          },
        },
        two: {
          dots: ["up-left", "down-right"],
          rotations: {
            x: -90,
            y: 0,
          },
          initRotation: {
            x: 90,
            y: 0,
          },
        },
        three: {
          dots: ["up-left", "center-center", "down-right"],
          rotations: {
            x: 0,
            y: 90,
          },
          initRotation: {
            x: 0,
            y: -90,
          },
        },
        four: {
          dots: ["up-left", "up-right", "down-left", "down-right"],
          rotations: {
            x: 0,
            y: -90,
          },
          initRotation: {
            x: 0,
            y: 90,
          },
        },
        five: {
          dots: [
            "up-left",
            "up-right",
            "down-left",
            "down-right",
            "center-center",
          ],
          rotations: {
            x: 90,
            y: 0,
          },
          initRotation: {
            x: -90,
            y: 0,
          },
        },
        six: {
          dots: [
            "up-left",
            "up-right",
            "down-left",
            "down-right",
            "center-left",
            "center-right",
          ],
          rotations: {
            x: 0,
            y: 180,
          },
          initRotation: {
            x: 0,
            y: 180,
          },
        },
      },

      style: {},
      diceStyle: {},
    };
  },
  mounted() {
    this.crateSides();
    this.createDotsCSS();
  },
  methods: {
    crateSides() {
      for (const [s, value] of Object.entries(this.config)) {
        let style = "";
        if (value.initRotation.x) {
          style += "rotateX(" + value.initRotation.x + "deg) ";
        }
        if (value.initRotation.y) {
          style += "rotateY(" + value.initRotation.y + "deg) ";
        }

        style += "translateZ(3.1em)";

        this.style[s] = {
          transform: style,
        };
      }
    },

    createDotsCSS() {
      let yCSSRules = {
        left: 20,
        right: 80,
        center: 50,
      };

      let xCSSRules = {
        up: 20,
        down: 80,
        center: 50,
      };

      for (const [y, yRule] of Object.entries(yCSSRules)) {
        for (const [x, xRule] of Object.entries(xCSSRules)) {
          this.style[x + "-" + y] =
            "left: " + xRule + "%; top: " + yRule + "%;";
        }
      }
    },

    rollDice(value) {
      this.value = value;

      this.diceStyle = {
        transform: this.getTransformation(value),
      };
    },

    getTransformation(number) {
      let style = "";

      let numberToString = {
        1: "one",
        2: "two",
        3: "three",
        4: "four",
        5: "five",
        6: "six",
      };

      let dice = this.config[numberToString[number]].rotations;

      let x, y;

      if (this.currX >= 0) {
        x = dice.x - 2 * 1440;
      } else {
        x = dice.x + 2 * 1440;
      }

      if (this.currY >= 0) {
        y = dice.y - 2 * 1440;
      } else {
        y = dice.y + 2 * 1440;
      }

      style += "rotateX(" + x + "deg) ";
      style += "rotateY(" + y + "deg)";

      // rotateZ

      this.currX += x;
      this.currY += y;

      return style;
    },
  },
};
</script> 
  
  <style>
#d {
  border-style: dotted;
}
</style>