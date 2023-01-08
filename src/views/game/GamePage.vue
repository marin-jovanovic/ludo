<template>
  <!-- style="border-style: solid" -->

  <BaseUserTemplate>
    <TheMessages></TheMessages>
    <!-- <TheInfo ref="info"></TheInfo> -->

    <div class="row">
      <div class="col">
        <TheGame @tokenSelected="userClickedOnToken" ref="level"></TheGame>
      </div>
    </div>

    <!-- <TheInfo ref="info"></TheInfo> -->

    <button @click="leaveGame">leave game</button>

    <div class="row">
      <div class="col"></div>

      <div class="col">
        <div class="row">
          <div class="col">
            <TheDice ref="dice"></TheDice>
          </div>
          <div class="col">
            <button @click="rollDice">roll dice</button>
          </div>
        </div>
      </div>

      <div class="col">
        <h5>join index: {{ this.joinId }}</h5>
        <h5>username: {{ this.username }}</h5>
      </div>
    </div>

    <table>
      <tr>
        <th>index</th>
        <th>entryId</th>
        <th>userJoinIndex</th>
        <th>action</th>
        <th>diceResult</th>
        <th>tokenId</th>
        <th>performed</th>
      </tr>

      <tr v-for="(i, index) in this.log" :key="index">
        <td>{{ index }}</td>
        <td>{{ i.entryId }}</td>
        <td>{{ i.userJoinIndex }}</td>
        <td>{{ i.action }}</td>
        <td>{{ i.diceResult }}</td>

        <td>{{ i.tokenId }}</td>
        <td>{{ i.performed }}</td>
      </tr>
    </table>

    all {{ this.lastExecutedByAll }}
    <br />
    any {{ this.lastExecutedByAny }}
    <br />
    this{{ this.lastExecutedThisUser }}

    <br />
    <button @click="this.tryNextInstruction">try next</button>

    <br />
    order:{{ this.order }}

    <br />
    <button v-if="this.isDone" @click="goToLevel">start game</button>
  </BaseUserTemplate>
</template>
<style>
table {
  font-family: arial, sans-serif;
  border-collapse: collapse;
  width: 100%;
}

td,
th {
  border: 1px solid #dddddd;
  text-align: left;
  padding: 8px;
}

tr:nth-child(even) {
  background-color: #dddddd;
}
</style>

<script>
// import TheInfo from "@/views/game/TheInfo.vue";
import TheDice from "@/components/TheDice.vue";
// import TheInfo from "./TheInfo.vue";
import TheGame from "./TheGame.vue";
import BaseUserTemplate from "@/components/BaseUserTemplate.vue";
import TheMessages from "@/views/game/TheMessages.vue";
import { apiLevelLog } from "@/scripts/api/level_log";

import { levelSessionStorage, userMetaSS } from "@/scripts/session_storage";
// import { apiLevel } from "@/scripts/api/level";
import { acceptanceLogApi } from "@/scripts/api/acceptance_log";
import { wsListeners } from "@/scripts/ws_listener";
import { notification } from "@/scripts/notification";
// import { setJoinIndex } from "@/scripts/set_playing_order";
// import { router } from "@/router/router";
import { apiLevel } from "@/scripts/api/level";
/**
 * currentEntryIndex = 0
 *
 * try perform it, if can perfrom then advance to next index
 *
 * this is different from dice order part
 *
 */

/**
       * do not use


         this.lastExecutedByAll,
         this is only to see if all users performed previous entries
         
       this.lastExecutedThisUser,
        this is to ???         

        this.lastExecutedByAny
        for confirmation


        ---------- entry 0 ---------- 
        1 <- instruction
          -> "ok"
        2 <- master done
        2 -> "ok"
        ------------------------
        1 <- "everyone confirmed"
        2 <- "everyone confirmed"
        1 -> "ok"
        2 -> "ok"

        ------------------------------------------------

        ---------- entry 1 ---------- 
        1 <- instruction
          -> "ok"
        2 <- master done
        2 -> "ok"
        ------------------------
        1 <- "everyone confirmed"
        2 <- "everyone confirmed"
        1 -> "ok"
        2 -> "ok"


        master role:

          everyone confirmed up till now?
          yes
            execute new "instruction"
            send "ok"
            wait for "everyone confirmed"
          no
            wait
          
          
        slave role:

          server sent "master done"?
          yes
            ...
            send "ok"
            wait for "everyone confirmed"
          no
            wait

       */

export default {
  data() {
    return {
      username: "",
      gameId: "",
      log: undefined,

      levelId: undefined,
      joinId: undefined,

      isWaitingForUserToChooseToken: false,

      // user: undefined,
      lastExecutedByAll: undefined,
      lastExecutedThisUser: undefined,
      lastExecutedByAny: undefined,

      order: {},

      isDone: false,

      isRolledAlready: false,

      trySuccessful: false,
    };
  },
  async mounted() {
    let flag = await this.$refs.level.initGame();
    // let flag = res["auth"]["status"] && res["payload"]["status"];

    if (!flag) {
      console.log("err");
      return;
    }

    this.levelId = this.$route.params.id;
    levelSessionStorage.set({ variable: "Id", value: this.levelId });

    let res = await apiLevel.getSpecificLevel({ levelId: this.levelId });

    flag = res["auth"]["status"] && res["payload"]["status"];

    if (!flag) {
      console.log("err");
      return;
    }

    levelSessionStorage.set({
      variable: "Capacity",
      value: Object.keys(res["payload"]["users"]).length,
    });

    console.log(levelSessionStorage.getLevelMeta());
    let capacity = levelSessionStorage.getLevelMeta()["capacity"];

    console.log("capacity", capacity);

    this.username = userMetaSS.getCredentials()["username"];

    for (const val of Object.values(res["payload"]["users"])) {
      if (val.username === this.username) {
        levelSessionStorage.set({
          variable: "JoinIndex",
          value: val.joinId,
        });
      }
    }

    this.joinId = levelSessionStorage.getLevelMeta()["levelJoinIndex"];

    let url = "ws://127.0.0.1:8000/acceptanceLogEntryCreated/";
    new wsListeners.WebSocketListener(url, this.wsReceive);

    // run condition, what if get then ws vs ws then get

    await this.loadLog();

    let r = await this.fetchLastExecuted();

    if (!r) {
      return;
    }

    await this.loadConfirmationLog();

    // await this.bypassGoes(this.levelId, capacity);

    await this.tryNextInstruction();
  },
  methods: {
    // check for goes
    // async bypassGoes(levelId, capacity) {
    //   // skip first part of the log where order is determined

    //   let log = this.log;

    //   let c = 0;
    //   let logIndex = 0;
    //   for (const value of Object.values(log)) {
    //     if (value.action === "goes") {
    //       c++;
    //     }

    //     if (capacity === c) {
    //       break;
    //     }
    //     logIndex++;
    //   }

    //   if (capacity !== c) {
    //     console.log("err capacity !== c", capacity, c);
    //   }

    //   console.log("mvoe forward to ", logIndex);

    //   // return logIndex;
    // },

    // this is from playing order

    addToOrder(orderObj) {
      console.log(orderObj);
      this.order[orderObj.userJoinIndex] = {
        orderObj,
      };
      let capacity = levelSessionStorage.getLevelMeta()["capacity"];
      console.log(this.order, this.order.size, capacity);

      let isOrderDetermined = capacity === Object.keys(this.order).length;
      if (isOrderDetermined) {
        let logEntry = this.getCurrentLogEntry();

        console.log("last what needs to be confirmed", logEntry);

        // this.isDoneNeedToConfirm = {
        //   entryId: logEntry.entryId,
        //   entryIndex: logEntry.entryIndex,
        // };

        // done only when all except one user won
        // this.isDone = true;
        // console.log("block any new movements");
      }
    },

    isMyTurn(logEntry) {
      return logEntry.userJoinIndex === this.joinId;
    },

    getCurrentLogEntry() {
      let lastIndexInLog = Object.keys(this.log).length - 1;
      let logEntry = this.log[lastIndexInLog];

      console.log("loge entry", logEntry);

      return logEntry;
    },

    async entryCleanup() {
      console.log("prepare for sending confirmation");
      let logEntry = this.getCurrentLogEntry();

      let isLogged = await this.sendConfirmation(logEntry.entryId);

      notification.showMessage(
        isLogged,
        "move logged",
        "error logging to server"
      );

      if (!isLogged) {
        console.log("err");
      }

      return isLogged;
    },

    async tryNextInstruction() {
      let logEntry = this.getCurrentLogEntry();

      console.log(
        this.isDone,
        this.lastExecutedByAll.entryIndex,
        logEntry.entryIndex
      );

      if (this.isDone) {
        console.log("done");
        return;
      }

      if (logEntry.performed) {
        console.log("already performed");
        return;
      }

      // 5 6
      if (!(this.lastExecutedByAll.entryIndex + 1 === logEntry.entryIndex)) {
        console.log(this.lastExecutedByAll.entryIndex, logEntry.entryIndex);
        return;
      }

      // 6 5 || 5 5
      if (
        !(
          this.lastExecutedByAny.entryIndex + 1 === logEntry.entryIndex ||
          this.lastExecutedByAny.entryIndex === logEntry.entryIndex
        )
      ) {
        console.log(this.lastExecutedByAny.entryIndex, logEntry.entryIndex);
        return;
      }

      // 4 5
      if (!(this.lastExecutedThisUser.entryIndex + 1 === logEntry.entryIndex)) {
        console.log(this.lastExecutedThisUser.entryIndex, logEntry.entryIndex);
        return;
      }

      if (this.lastExecutedThisUser.entryIndex >= logEntry.entryIndex) {
        console.log("err implementation, i have execute this already");
        return;
      }

      console.log(this.lastExecutedThisUser.entryIndex, logEntry.entryIndex);

      // >=
      if (this.lastExecutedThisUser.entryIndex > logEntry.entryIndex) {
        console.log("this is executed by this user already");
        return;
      } else {
        console.log("ok, this index is bigger or eq");
      }

      console.log("log entry", logEntry);

      if (!this.isMyTurn(logEntry)) {
        console.log("role: slave");

        // someone else performed this instruction
        // if true than it is master
        // i can perform this instruction

        let masterEntryIndex = this.lastExecutedByAny.entryIndex;
        console.log(masterEntryIndex);

        if (masterEntryIndex >= logEntry.entryIndex) {
          console.log("master executed >=");
        } else {
          console.log("not yet executed");
          return;
        }
      }

      if (this.isMyTurn(logEntry)) {
        // my turn

        switch (logEntry.action) {
          case "roll":
            console.log("role: master");
            console.log("can not auto execute my roll");

            await this.rollDice();

            break;

          case "goes":
            console.log("can auto goes", logEntry);

            this.addToOrder({
              username: this.username,
              userJoinIndex: logEntry.userJoinIndex,
            });
            await this.entryCleanup();

            break;

          case "choose":
            console.log("can not auto choose");
            break;

          case "move":
            console.log("i have to auto move my token");

            this.$refs.level.movePosition(
              logEntry.userJoinIndex,
              logEntry.tokenId,
              logEntry.diceResult
            );

            await this.entryCleanup();

            break;

          case "eaten":
            console.log("auto eat, canvas does this auto");
            await this.entryCleanup();
            break;

          case "won":
            alert("you have won the level");
            this.isDone = true;
            break;

          default:
            console.log("unknown action", logEntry.action);
            break;
        }
      } else {
        // other player choose

        switch (logEntry.action) {
          case "roll":
            console.log("master executed roll");

            this.$refs.dice.rollDice(logEntry.diceResult);

            await this.entryCleanup();

            break;

          case "goes":
            console.log("goes", logEntry);

            this.addToOrder({
              username: this.username,
              userJoinIndex: logEntry.userJoinIndex,
            });
            await this.entryCleanup();

            break;
          case "choose":
            console.log("master has choosen");

            await this.entryCleanup();

            break;

          case "move":
            console.log("i have to auto move someone elses token");
            this.$refs.level.movePosition(
              logEntry.userJoinIndex,
              logEntry.tokenId,
              logEntry.diceResult
            );

            await this.entryCleanup();

            break;

          case "eaten":
            console.log("auto eat, canvas does this auto");
            await this.entryCleanup();
            break;

          default:
            console.log("err unknown action", logEntry.action);
            break;
        }
      }
    },

    // passive actions
    async wsReceive(message) {
      console.log("received update", message);
      await this.loadLog();

      if (this.isDone) {
        console.log("--- done");
        return;
      }

      let lastExecuted = {
        status: true,
        entryIndex: Number(message.entryIndex),
        entryId: Number(message.entryId),
      };

      if (message.type === "firstReceived") {
        console.log("firstReceived");

        // all stays the same
        // this is changed to this if received from this user

        if (this.lastExecutedByAny.entryIndex < lastExecuted.entryIndex) {
          this.lastExecutedByAny = lastExecuted;
        } else {
          console.log("err: this does not make sense");
        }

        if (this.username === message.userUsername) {
          console.log("this usernaem");

          this.lastExecutedThisUser = lastExecuted;
        } else {
          console.log("other user");
        }

        // no need to try next instruction because this one is not yet confirmed
      } else if (message.type === "allReceived") {
        console.log("allReceived");

        this.isRolledAlready = false;

        if (this.lastExecutedByAny.entryIndex < lastExecuted.entryIndex) {
          this.lastExecutedByAny = lastExecuted;
        } else {
          // maybe sending previous instruction
          console.log("err: this does not make sense");
        }

        if (this.lastExecutedByAll.entryIndex < lastExecuted.entryIndex) {
          this.lastExecutedByAll = lastExecuted;
        } else {
          console.log("err: this does not make sense");
        }

        // no need to check
        this.lastExecutedThisUser = lastExecuted;
      } else {
        console.log("err unknown");
        return;
      }

      this.trySuccessful = false;
      await this.tryNextInstruction();
    },

    async fetchLastExecuted() {
      const res = await acceptanceLogApi.getAcceptanceLogForLevel({
        levelId: this.levelId,
      });
      const flag = res["auth"]["status"] && res["payload"]["status"];
      if (!flag) {
        console.log("err, try fetch from api again");
        return false;
      }
      this.lastExecutedByAll = res["payload"]["lastExecutedByAll"];
      this.lastExecutedThisUser = res["payload"]["lastExecutedThisUser"];
      this.lastExecutedByAny = res["payload"]["lastExecutedByAny"];
      const lastExecuted = { status: true, entryIndex: -1, entryId: undefined };
      if (!this.lastExecutedByAll.status) this.lastExecutedByAll = lastExecuted;
      if (!this.lastExecutedByAny.status) this.lastExecutedByAny = lastExecuted;
      if (!this.lastExecutedThisUser.status)
        this.lastExecutedThisUser = lastExecuted;
      return true;
    },
    // if page refreshed
    async loadConfirmationLog() {
      /**
      if all is empty
        non confirmed - maybe master send something, do not use this
        
      if user
        this one did not perform anything 

       */

      // do all until lastExecutedThisUser
      for (const [i, logEntry] of Object.entries(this.log)) {
        console.log(i, logEntry);

        if (this.isDone) {
          console.log("--- done");
          return;
        }

        console.log("fast reload", i, this.lastExecutedThisUser.entryIndex);

        if (Number(i) > this.lastExecutedThisUser.entryIndex) {
          // this user did not execute this yet

          console.log("i have not yet executed this");

          if (Number(i) <= this.lastExecutedByAny.entryIndex) {
            console.log("master executed this");

            switch (logEntry.action) {
              case "roll":
                this.$refs.dice.rollDice(logEntry.diceResult);
                break;
              case "goes":
                console.log("goes", logEntry);
                this.addToOrder({
                  username: "todo",
                  userJoinIndex: logEntry.userJoinIndex,
                });
                break;

              case "choose":
                console.log("choose");
                break;

              case "move":
                console.log("------------- mvoe");

                this.$refs.level.movePosition(
                  logEntry.userJoinIndex,
                  logEntry.tokenId,
                  logEntry.diceResult
                );

                break;
              case "eaten":
                console.log("auto eat, canvas does this auto");
                break;
              default:
                console.log("err");
                console.log("fast setup", i, logEntry);
                console.log("unknow action", logEntry.action);
                return;
            }
            const isLogged = await this.sendConfirmation(logEntry.entryId);
            notification.showMessage(
              isLogged,
              "move logged",
              "error logging to server"
            );
            if (!isLogged) console.log("err api call");
          } else {
            console.log("master also did not execute this");
          }
        } else {
          // this user did execute this yet
          console.log("already executed this");

          switch (logEntry.action) {
            case "roll":
              this.$refs.dice.rollDice(logEntry.diceResult);
              break;
            case "goes":
              console.log("goes", logEntry);
              this.addToOrder({
                username: "todo",
                userJoinIndex: logEntry.userJoinIndex,
              });
              break;

            case "choose":
              console.log("choose");
              break;

            case "move":
              console.log("------------- mvoe did this", logEntry);

              this.$refs.level.movePosition(
                logEntry.userJoinIndex,
                logEntry.tokenId,
                logEntry.diceResult
              );

              break;
            case "eaten":
              console.log("auto eat, canvas does this auto");
              break;
            default:
              console.log("fast setup", i, logEntry);
              console.log("unknow action", logEntry.action);
              return;
          }

          // no need for sending confirmation, i have already executed this
        }
      }

      return;
    },

    async sendConfirmation(entryId) {
      console.log("confirmation for", entryId);
      const res = await acceptanceLogApi.addEntryToAcceptanceLog({
        levelId: this.levelId,
        entryId: entryId,
      });
      const flag = res["auth"]["status"] && res["payload"]["status"];

      if (!flag) console.log("err", res);

      return flag;
    },

    manualActionsPre() {
      if (this.isDone) {
        console.log("--- done");
        return false;
      }

      let logEntry = this.getCurrentLogEntry();

      // if (this.lastExecutedByAll.status) {
      if (this.lastExecutedByAll.entryIndex !== logEntry.entryIndex - 1) {
        console.log("small, previos is not yet confirmed");

        return false;
      }
      // }
      //
      if (!this.isMyTurn(logEntry)) {
        console.log("not your turn");
        notification.showMessage(false, "", "not your turn");
        return false;
      }

      return true;
    },

    async rollDice() {
      if (this.isRolledAlready) {
        console.log("rolled already");
        return;
      }

      let t = this.manualActionsPre();

      if (!t) {
        return;
      }

      let logEntry = this.getCurrentLogEntry();

      if (logEntry.action !== "roll") {
        console.log("not roll action", logEntry.action);
        return;
      }

      this.isRolledAlready = true;

      this.$refs.dice.rollDice(logEntry.diceResult);

      console.log("roll ok");

      // todo
      this.entryCleanup();
    },

    async userClickedOnToken(username, tokenId) {
      // no need for additional checks, assumption is that they are run in previous function

      console.log("user clicked on token", username, tokenId);

      let t = this.manualActionsPre();

      if (!t) {
        return;
      }

      let logEntry = this.getCurrentLogEntry();

      if (logEntry.action !== "choose") {
        console.log("not choose action", logEntry.action);

        return;
      }

      if (this.username !== username) {
        console.log(
          "not same usernmae, choose your tokens",
          this.username,
          username
        );

        notification.showMessage(false, "", "choose your tokens");

        return;
      }

      let res = await apiLevelLog.addToLog(
        this.levelId,
        tokenId,
        logEntry.entryId
      );

      if (!(res["auth"]["status"] && res["payload"]["status"])) {
        console.log("err");
        return;
      }

      this.entryCleanup();
      this.$refs.level.movePosition(
        logEntry.userJoinIndex,
        logEntry.tokenId,
        logEntry.diceResult
      );

      this.tryNextInstruction();
    },

    async loadLog() {
      let res = await apiLevelLog.getLevelLog(this.levelId);

      if (!(res["auth"]["status"] && res["payload"]["status"])) {
        console.log("err");
        return;
      }

      this.log = res["payload"]["log"];
    },
  },
  components: {
    // TheInfo,
    TheDice,
    BaseUserTemplate,
    TheMessages,

    // TheInfo,
    TheGame,
  },
};
</script> 
