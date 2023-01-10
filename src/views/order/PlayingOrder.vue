<template>
  <!-- style="border-style: solid" -->

  <BaseUserTemplate>
    <TheMessages></TheMessages>
    <!-- <TheInfo ref="info"></TheInfo> -->

    <button @click="leaveGame">leave game</button>

    <div class="row">
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

import BaseUserTemplate from "@/components/BaseUserTemplate.vue";
import TheMessages from "@/views/game/TheMessages.vue";
import { apiLevelLog } from "@/scripts/api/level_log";

import { levelSessionStorage, userMetaSS } from "@/scripts/session_storage";
// import { apiLevel } from "@/scripts/api/level";
import { acceptanceLogApi } from "@/scripts/api/acceptance_log";
import { wsListeners } from "@/scripts/ws_listener";
import { notification } from "@/scripts/notification";
// import { setJoinIndex } from "@/scripts/set_playing_order";
import { router } from "@/router/router";
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
      isDoneNeedToConfirm: {},
    };
  },
  async mounted() {
    this.isDoneNeedToConfirm.entryIndex = Number.MAX_SAFE_INTEGER;

    this.levelId = this.$route.params.id;
    levelSessionStorage.set({ variable: "Id", value: this.levelId });

    let res = await apiLevel.getSpecificLevel({ levelId: this.levelId });

    levelSessionStorage.set({
      variable: "Capacity",
      value: Object.keys(res["users"]).length,
    });

    // userMetaSS.se

    this.username = userMetaSS.getCredentials()["username"];

    for (const val of Object.values(res["users"])) {
      // console.log(key, value);
      if (val.username === this.username) {
        levelSessionStorage.set({
          variable: "JoinIndex",
          value: val.joinId,
        });
      }
    }

    // await setJoinIndex(this.username, this.levelId);

    this.joinId = levelSessionStorage.getLevelMeta()["levelJoinIndex"];

    // this.currentLogEntryIndex = await this.bypassGoes(this.levelId, capacity);

    // console.log(capacity);

    // this.currentLogEntryIndex = 0;

    let url =
      "ws://" + process.env.VUE_APP_BACKEND_WS + "/acceptanceLogEntryCreated/";

    new wsListeners.WebSocketListener(url, this.wsReceive);

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
    goToLevel() {
      console.log("to game", this.levelId);
      // conso

      router.replace(`/game/${this.levelId}`);
    },

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

        this.isDoneNeedToConfirm = {
          entryId: logEntry.entryId,
          entryIndex: logEntry.entryIndex,
        };

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
      // console.log("entryCleanup");

      console.log("prepare for sending confirmation");
      let logEntry = this.getCurrentLogEntry();

      let isLogged = await this.sendConfirmation(logEntry.entryId);

      notification.showMessage(
        isLogged,
        "move logged",
        "error logging to server"
      );

      if (!isLogged) {
        // console.log(
        //   "logged, now wait for confirmation that all others did this"
        // );
        // or this.currentLogEntryIndex = entryLogIndex
        // this.currentLogEntryIndex++;
        // } else {
        console.log("err");
      }
    },

    async tryNextInstruction() {
      let logEntry = this.getCurrentLogEntry();

      console.log(
        this.isDone,
        this.lastExecutedByAll.entryIndex,
        this.isDoneNeedToConfirm.entryIndex,
        this.lastExecutedByAll.entryIndex >= this.isDoneNeedToConfirm.entryIndex
      );

      if (
        this.isDone &&
        this.lastExecutedByAll.entryIndex >= this.isDoneNeedToConfirm.entryIndex
      ) {
        console.log("--- done");
        return;
      }

      console.log(this.lastExecutedThisUser.entryIndex, logEntry.entryIndex);

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
        switch (logEntry.action) {
          case "roll":
            console.log("role: master");
            console.log("can not auto execute my roll");
            break;

          case "goes":
            console.log("goes", logEntry);

            this.addToOrder({
              username: this.username,
              userJoinIndex: logEntry.userJoinIndex,
            });
            await this.entryCleanup();

            break;

          default:
            console.log("unknown action", logEntry.action);
            break;
        }
      } else {
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

          default:
            console.log("unknown action", logEntry.action);
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

      console.log(
        this.lastExecutedByAll,
        this.lastExecutedThisUser,
        this.lastExecutedByAny
      );

      let lastExecuted = {
        status: true,
        entryIndex: Number(message.entryIndex),
        entryId: Number(message.entryId),
      };

      if (message.type === "firstReceived") {
        console.log("firstReceived");

        // all stays the same
        // this is changed to this if received from this user

        if (
          !this.lastExecutedByAny.status ||
          this.lastExecutedByAny.entryIndex < lastExecuted.entryIndex
        ) {
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

        if (
          !this.lastExecutedByAny.status ||
          this.lastExecutedByAny.entryIndex < lastExecuted.entryIndex
        ) {
          this.lastExecutedByAny = lastExecuted;
        } else {
          console.log("err: this does not make sense");
        }

        if (
          !this.lastExecutedByAll.status ||
          this.lastExecutedByAll.entryIndex < lastExecuted.entryIndex
        ) {
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

    // if page refreshed
    async loadConfirmationLog() {
      let res = await acceptanceLogApi.getAcceptanceLogForLevel({
        levelId: this.levelId,
      });

      this.lastExecutedByAll = res["lastExecutedByAll"];
      this.lastExecutedThisUser = res["lastExecutedThisUser"];
      this.lastExecutedByAny = res["lastExecutedByAny"];

      let lastExecuted = {
        status: true,
        entryIndex: Number(-1),
        entryId: undefined,
      };

      if (!this.lastExecutedByAll.status) {
        this.lastExecutedByAll = lastExecuted;
      }
      if (!this.lastExecutedByAny.status) {
        this.lastExecutedByAny = lastExecuted;
      }
      if (!this.lastExecutedThisUser.status) {
        this.lastExecutedThisUser = lastExecuted;
      }

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

              // await this.entryCleanup();
              let isLogged = await this.sendConfirmation(logEntry.entryId);

              notification.showMessage(
                isLogged,
                "move logged",
                "error logging to server"
              );

              if (!isLogged) {
                console.log("err");
              }

              this.addToOrder({
                username: "todo",
                userJoinIndex: logEntry.userJoinIndex,
              });
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

            let isLogged = await this.sendConfirmation(logEntry.entryId);

            notification.showMessage(
              isLogged,
              "move logged",
              "error logging to server"
            );

            if (!isLogged) {
              console.log("err");
            }

            this.addToOrder({
              username: "todo",
              userJoinIndex: logEntry.userJoinIndex,
            });
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

      await acceptanceLogApi.addEntryToAcceptanceLog({
        levelId: this.levelId,
        entryId: entryId,
      });

      return true;
    },

    async rollDice() {
      if (this.isRolledAlready) {
        console.log("rolled already");
        return;
      }

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

      this.isRolledAlready = true;

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

    async loadLog() {
      let res = await apiLevelLog.getLevelLog(this.levelId);

      // console.log("log (accepted + 1st unaccepted)", res["payload"]["log"]);

      this.log = res["log"];

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
