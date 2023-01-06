<template>
  <!-- style="border-style: solid" -->

  <BaseUserTemplate>
    <TheMessages></TheMessages>
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
    <button v-if="this.isDone">start game</button>
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

import BaseUserTemplate from "@/components/BaseUserTemplate.vue";
import TheMessages from "@/views/game/TheMessages.vue";
import { apiLevelLog } from "@/scripts/api/level_log";

import { levelSessionStorage, userMetaSS } from "@/scripts/session_storage";
// import { apiLevel } from "@/scripts/api/level";
import { acceptanceLogApi } from "@/scripts/api/acceptance_log";
// import { wsListeners } from "@/scripts/ws_listener";
import { notification } from "@/scripts/notification";
// import { setJoinIndex } from "@/scripts/set_playing_order";

/**
 * currentEntryIndex = 0
 *
 * try perform it, if can perfrom then advance to next index
 *
 * this is different from dice order part
 *
 */

export default {
  data() {
    return {
      username: "",
      gameId: "",
      log: undefined,

      levelId: undefined,
      // players: {},
      joinId: undefined,
      // currentLogEntryIndex: 0,
      // globalPerformedLogEntryIndexToId: undefined,
      // privatePerformedLogEntryIndexToId: undefined,
      isWaitingForUserToChooseToken: false,

      // user: undefined,
      lastExecutedByAll: undefined,
      lastExecutedThisUser: undefined,
      lastExecutedByAny: undefined,

      order: [],

      isDone: false,
    };
  },
  async mounted() {
    this.levelId = this.$route.params.id;
    this.username = userMetaSS.getCredentials()["username"];

    // await setJoinIndex(this.username, this.levelId);

    this.joinId = levelSessionStorage.getLevelMeta()["levelJoinIndex"];

    // this.currentLogEntryIndex = await this.bypassGoes(this.levelId, capacity);

    // console.log(capacity);

    // this.currentLogEntryIndex = 0;

    // todo this late
    // let url = "ws://127.0.0.1:8000/acceptanceLogEntryCreated/";
    // new wsListeners.WebSocketListener(url, this.wsReceive);

    // run condition, what if get then ws vs ws then get

    // await this.loadPlayers();
    await this.loadLog();

    await this.loadConfirmationLog();

    // console.log("this user", this.joinId);

    console.log(
      this.lastExecutedByAll,
      this.lastExecutedThisUser,
      this.lastExecutedByAny
    );

    await this.tryNextInstruction();
  },
  methods: {
    // check for goes
    // async bypassGoes(levelId, capacity) {
    //   // skip first part of the log where order is determined
    //   let res = await apiLevelLog.getLevelLog(levelId);

    //   if (!(res["auth"]["status"] && res["payload"]["status"])) {
    //     console.log("err");
    //     return;
    //   }

    //   let log = res["payload"]["log"];

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

    //   return logIndex;
    // },

    // this is from playing order

    addToOrder(orderObj) {
      this.order.push(orderObj);

      let capacity = levelSessionStorage.getLevelMeta()["capacity"];

      let isOrderDetermined = capacity === this.order.length;

      if (isOrderDetermined) {
        this.isDone = true;
        console.log("block any new movements");
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
      console.log("entryCleanup");
      let logEntry = this.getCurrentLogEntry();

      let isLogged = await this.sendConfirmation(logEntry.entryId);

      notification.showMessage(
        isLogged,
        "move logged",
        "error logging to server"
      );

      if (isLogged) {
        console.log(
          "logged, now wait for confirmation that all others did this"
        );
        // or this.currentLogEntryIndex = entryLogIndex
        // this.currentLogEntryIndex++;
      } else {
        console.log("err");
      }
    },

    async tryNextInstruction() {
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

      console.log("todo try next instruction");

      if (this.isDone) {
        console.log("--- done");
        return;
      }

      let logEntry = this.getCurrentLogEntry();

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

      if (logEntry.action === "roll" && !this.isMyTurn(logEntry)) {
        console.log("master executed roll");
        console.log("role: slave");

        this.$refs.dice.rollDice(logEntry.diceResult);

        // send confirmation
        await this.entryCleanup();
        return;
      } else if (logEntry.action === "roll" && this.isMyTurn(logEntry)) {
        console.log("role: master");
        console.log("can not auto execute my roll");
        return;
      } else if (this.isMyTurn(logEntry) && logEntry.action === "goes") {
        console.log("goes", logEntry);

        this.addToOrder({
          username: this.username,
          userJoinIndex: logEntry.userJoinIndex,
        });

        await this.entryCleanup();
        return;
      } else {
        // if (logEntry.action === "roll") {
        //   console.log("can not perform roll auto, user needs to click dice");
        //   return;
        // } else {
        console.log("unknown action", logEntry.action);
        return;
      }

      // for (const [i, logEntry] of Object.entries(this.log)) {
      //   console.log(i, logEntry);

      //   console.log("fast reload", i, this.lastExecutedThisUser.entryIndex);

      //   if (Number(i) > this.lastExecutedThisUser.entryIndex) {
      //     // this user did not execute this yet

      //     console.log("i have not yet executed this");

      //     if (Number(i) <= this.lastExecutedByAny.entryIndex) {
      //       console.log("master executed this");

      //       if (logEntry.action === "roll") {
      //         this.$refs.dice.rollDice(logEntry.diceResult);

      //         let isLogged = await this.sendConfirmation(logEntry.entryId);

      //         notification.showMessage(
      //           isLogged,
      //           "move logged",
      //           "error logging to server"
      //         );

      //         if (!isLogged) {
      //           console.log("err");
      //         }
      //       } else {
      //         console.log("err");
      //         console.log("fast setup", i, logEntry);
      //         console.log("unknow action", logEntry.action);
      //       }
      //     } else {
      //       console.log("master also did not execute this");
      //     }
      //   } else {
      //     // this user did execute this yet

      //     if (logEntry.action === "roll") {
      //       this.$refs.dice.rollDice(logEntry.diceResult);

      //       let isLogged = await this.sendConfirmation(logEntry.entryId);

      //       notification.showMessage(
      //         isLogged,
      //         "move logged",
      //         "error logging to server"
      //       );

      //       if (!isLogged) {
      //         console.log("err");
      //       }
      //     } else {
      //       console.log("fast setup", i, logEntry);
      //       console.log("unknow action", logEntry.action);
      //     }
      //   }
      // }

      // return;

      // if (logEntry.player !== this.joinId) {
      //   if (logEntry.instruction_id in this.globalPerformedLogEntryIndexToId) {
      //     console.log("master made this instruction");
      //   } else {
      //     console.log("need to wait for master player to log this move");
      //     return;
      //   }
      // }

      // // main

      // if (logEntry.action === "goes") {
      //   console.log("err tryNextInstruction goes");
      // } else if (logEntry.action === "move") {
      //   console.log("move", logEntry);

      //   if (this.joinId !== logEntry.player) {
      //     console.log("err not same", this.joinId, logEntry.player);
      //   }

      //   this.$refs.level.movePosition({
      //     player: logEntry.player,
      //     token: logEntry.token,
      //     jumpCount: logEntry.diceResult,
      //   });
      // } else if (
      //   logEntry.player !== this.joinId &&
      //   logEntry.action === "roll"
      // ) {
      //   console.log("roll");
      //   this.$refs.dice.rollDice(logEntry.diceResult);
      // } else {
      //   console.log("tryNextInstruction can not perform on my own", logEntry);
      //   return;
      // }

      // this.entryCleanup(logEntry);
    },

    // passive actions
    async wsReceive(message) {
      console.log("received update", message);

      if (this.isDone) {
        console.log("--- done");
        return;
      }

      // todo check if this key exists then sorting problem (? assumption that this is cause)

      // todo this is not nice naming, change this to reflect it better
      // this.globalPerformedLogEntryIndexToId[message.id] = message.entryId;

      // await this.tryNextInstruction();

      // how does it know that it can contine?

      // let toAcceptIndex = message.entryId;

      // if (this.currentLogEntryIndex > Number(toAcceptIndex)) {
      //   console.log(this.currentLogEntryIndex, toAcceptIndex);
      //   console.log("mismatch, skip");
      //   await this.tryNextInstruction();
      //   return;
      // }

      // let logEntry = this.log[this.currentLogEntryIndex];
      // this.players[logEntry.player].isTurn = true;

      // if (logEntry.action === "roll") {
      //   // someone else performed this
      //   this.$refs.dice.rollDice(logEntry.diceResult);
      // }

      // this.currentLogEntryIndex++;
      // this.players[logEntry.player].isTurn = false;

      // // send to backend that it is performed
      // await this.sendConfirmation(this.currentLogEntryIndex - 1);

      // logEntry = this.log[this.currentLogEntryIndex];
      // this.players[logEntry.player].isTurn = true;

      // await this.tryNextInstruction();
    },

    // async fetchPerformedLogEntryIndexToId() {
    //   let res = await acceptanceLogApi.getAcceptanceLogForLevel({
    //     levelId: this.levelId,
    //   });

    //   let flag = res["auth"]["status"] && res["payload"]["status"];

    //   if (!flag) {
    //     console.log("err");
    //   }

    //   // console.log(res["payload"]);

    //   // return {}

    //   // this.globalPerformedLogEntryIndexToId =
    //   //   res["payload"]["globalPerformedEntries"];
    //   // this.privatePerformedLogEntryIndexToId =
    //   //   res["payload"]["performedEntries"];

    //   // console.log(Object.keys(res["payload"]["globalPerformedEntries"]).length);

    //   // console.log(Object.keys(res["payload"]["performedEntries"]).length);

    //   // return res["payload"]["performedEntries"];
    // },

    // if page refreshed
    async loadConfirmationLog() {
      let res = await acceptanceLogApi.getAcceptanceLogForLevel({
        levelId: this.levelId,
      });

      let flag = res["auth"]["status"] && res["payload"]["status"];

      if (!flag) {
        console.log("err");
      }

      this.lastExecutedByAll = res["payload"]["lastExecutedByAll"];
      this.lastExecutedThisUser = res["payload"]["lastExecutedThisUser"];
      this.lastExecutedByAny = res["payload"]["lastExecutedByAny"];

      /**
      if all is empty
        non confirmed - maybe master send something, do not use this
        
      if user
        this one did not perform anything 

       */

      if (!this.lastExecutedByAny.status) {
        /*
        master did not execute first entry
        */

        console.log("lastExecutedByAny empty");
        return;
      }

      // if ()

      console.log(this.lastExecutedThisUser);

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

            if (logEntry.action === "roll") {
              this.$refs.dice.rollDice(logEntry.diceResult);

              let isLogged = await this.sendConfirmation(logEntry.entryId);

              notification.showMessage(
                isLogged,
                "move logged",
                "error logging to server"
              );

              if (!isLogged) {
                console.log("err");
              }
            } else if (logEntry.action === "goes") {
              console.log("goes", logEntry);
              this.addToOrder({
                username: "todo",
                userJoinIndex: logEntry.userJoinIndex,
              });

              let isLogged = await this.sendConfirmation(logEntry.entryId);

              notification.showMessage(
                isLogged,
                "move logged",
                "error logging to server"
              );

              if (!isLogged) {
                console.log("err");
              }
            } else {
              console.log("err");
              console.log("fast setup", i, logEntry);
              console.log("unknow action", logEntry.action);
            }
          } else {
            console.log("master also did not execute this");
          }
        } else {
          // this user did execute this yet
          console.log("already executed this");

          if (logEntry.action === "roll") {
            this.$refs.dice.rollDice(logEntry.diceResult);

            let isLogged = await this.sendConfirmation(logEntry.entryId);

            notification.showMessage(
              isLogged,
              "move logged",
              "error logging to server"
            );

            if (!isLogged) {
              console.log("err");
            }
          } else if (logEntry.action === "goes") {
            console.log("goes", logEntry);
            this.addToOrder({
              username: "todo",
              userJoinIndex: logEntry.userJoinIndex,
            });

            let isLogged = await this.sendConfirmation(logEntry.entryId);

            notification.showMessage(
              isLogged,
              "move logged",
              "error logging to server"
            );

            if (!isLogged) {
              console.log("err");
            }
          } else {
            console.log("fast setup", i, logEntry);
            console.log("unknow action", logEntry.action);
          }
        }
      }

      return;

      // // console.log(res["payload"]);

      // let performedLogEntryIndexToId =
      //   await this.fetchPerformedLogEntryIndexToId();

      // console.log("ui updated", Object.keys(performedLogEntryIndexToId));

      // console.log("starting confirmation log with", this.currentLogEntryIndex);

      // // confirm everything before this
      // for (let i = 0; i < this.currentLogEntryIndex + 1; i++) {
      //   // console.log("auto confirm this", i, this.log[i].id);

      //   let isLogged = await this.sendConfirmation(this.log[i].id);

      //   if (!isLogged) {
      //     console.log("err sending confirmation");
      //   }
      // }

      // // add those instructions to performed entries
      // // this is executed instead of calling again fetchPerformedLogEntryIndexToId
      // for (let i = 0; i < this.currentLogEntryIndex + 1; i++) {
      //   // console.log("auto add this", i, this.log[i].id);

      //   // todo check if something diff is here then this is not correctly implemented (possible error while sorting?)
      //   performedLogEntryIndexToId[i] = this.log[i].id;
      // }

      // // fast loading (updating board)
      // for (const [i, logEntry] of Object.entries(this.log)) {
      //   if (Number(i) !== logEntry.instruction_id) {
      //     console.log("sorting error", Number(i), logEntry.instruction_id);
      //   }

      //   if (this.currentLogEntryIndex >= i) {
      //     // console.log(
      //     //   "skip (pre goes instruction)",
      //     //   this.currentLogEntryIndex,
      //     //   i
      //     // );
      //     continue;
      //   }

      //   if (!(i in performedLogEntryIndexToId)) {
      //     // console.log("logEntry not yet performed", i, logEntry);
      //     break;
      //   }

      //   console.log("fast perform", i, logEntry);

      //   switch (logEntry.action) {
      //     case "roll":
      //       this.$refs.dice.rollDice(logEntry.diceResult);

      //       break;
      //     case "goes":
      //       console.log("err goes");
      //       break;

      //     case "move":
      //       if (this.joinId !== logEntry.player) {
      //         console.log("err not same", this.joinId, logEntry.player);
      //       }

      //       this.$refs.level.movePosition({
      //         player: logEntry.player,
      //         token: logEntry.token,
      //         jumpCount: logEntry.diceResult,
      //       });

      //       break;

      //     default:
      //       console.log("err unknown");
      //       break;
      //   }

      //   // this.currentLogEntryIndex++;
      // }

      // this.currentLogEntryIndex =
      //   Object.keys(performedLogEntryIndexToId).length - 1;

      // console.log(
      //   "after fast reloading, last executed is",
      //   this.currentLogEntryIndex
      // );

      // // console.log(
      // //   "after realoding, we can be sure this is performed:",
      // //   Object.keys(this.privatePerformedLogEntryIndexToId),
      // // );
    },

    async sendConfirmation(entryId) {
      console.log("confirmation for", entryId);

      let res = await acceptanceLogApi.addEntryToAcceptanceLog({
        levelId: this.levelId,
        entryId: entryId,
      });

      let flag = res["auth"]["status"] && res["payload"]["status"];

      if (!flag) {
        console.log("err", res);
      }

      return flag;
    },

    async rollDice() {
      if (this.isDone) {
        console.log("--- done");
        return;
      }

      let logEntry = this.getCurrentLogEntry();

      if (this.lastExecutedByAll.status) {
        if (this.lastExecutedByAll.entryIndex !== logEntry.entryIndex - 1) {
          console.log("small");

          return;
        }
      }

      if (!this.isMyTurn(logEntry)) {
        console.log("not your turn");
        notification.showMessage(false, "", "not your turn");
        return;
      }

      if (logEntry.action !== "roll") {
        console.log("not roll action", logEntry.action);
        return;
      }

      this.$refs.dice.rollDice(logEntry.diceResult);

      console.log("roll ok");

      // todo
      this.entryCleanup();

      // console.log(
      //   this.currentLogEntryIndex + 1,
      //   this.log,
      //   this.currentLogEntryIndex + 1 in this.log
      // );

      // console.log(
      //   "todo determine if neeed to send payload (move token or not)"
      // );

      // if (
      //   !(this.currentLogEntryIndex + 1 + 1 in this.log) ||
      //   !(
      //     this.currentLogEntryIndex + 1 in
      //     this.privatePerformedLogEntryIndexToId
      //   )
      // ) {
      //   console.log("assumption: user needs to decide");

      //   this.isWaitingForUserToChooseToken = true;
      // } else {
      //   console.log("assumption: not used");

      //   this.entryCleanup(logEntry);
      // }

      // todo what if user reloads page now?

      // no cleanup

      // backend needs to send to others this info
      // backend waits for all others to confirm (timeout)
    },

    async userClickedOnToken(username, tokenId) {
      // no need for additional checks, assumption is that they are run in previous function

      console.log("user clicked on token", username, tokenId);

      if (this.isDone) {
        console.log("--- done");
        return;
      }

      console.log("todo");
      return;

      // if (
      //   !(this.currentLogEntryIndex + 1 + 1 in this.log) ||
      //   !(
      //     this.currentLogEntryIndex + 1 in
      //     this.privatePerformedLogEntryIndexToId
      //   )
      // ) {
      //   console.log("test: user needs to decide");

      //   this.isWaitingForUserToChooseToken = true;
      // } else {
      //   console.log("test: not used");
      // }

      // if (!this.isWaitingForUserToChooseToken) {
      //   console.log("not waiting for this");
      //   return;
      // }

      // if (this.username !== username) {
      //   console.log(
      //     "not same usernmae, choose your tokens",
      //     this.username,
      //     username
      //   );
      //   return;
      // }

      // this.isWaitingForUserToChooseToken = false;

      // // do this step again
      // let logEntry = this.entrySetup();

      // let t = await apiLevelLog.addToLog(this.levelId, tokenId);
      // console.log(t);

      // this.entryCleanup(logEntry, {
      //   instruction: "moveToken",
      //   username: username,
      //   tokenId: tokenId,
      // });
    },

    // async loadPlayers() {
    //   let res = await apiLevel.getSpecificLevel({ levelId: this.levelId });

    //   if (!(res["auth"]["status"] && res["payload"]["status"])) {
    //     console.log("err", res);
    //     return;
    //   }

    //   for (const [key, value] of Object.entries(res["payload"]["users"])) {
    //     // no need for isTurn -> todo remove
    //     this.players[value.joinId] = {
    //       username: value.username,
    //       isTurn: false,
    //       id: key,
    //     };
    //   }
    // },

    async loadLog() {
      let res = await apiLevelLog.getLevelLog(this.levelId);

      if (!(res["auth"]["status"] && res["payload"]["status"])) {
        console.log("err");
        return;
      }

      console.log("log (accepted + 1st unaccepted)", res["payload"]["log"]);

      this.log = res["payload"]["log"];

      // for (const [i, logEntry] of Object.entries(res["payload"]["log"])) {
      //   this.log[i] = logEntry;
      // }
    },
  },
  components: {
    // TheInfo,
    TheDice,
    BaseUserTemplate,
    TheMessages,
  },
};
</script> 
