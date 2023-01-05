import {
    apiLevel
} from "./api/level";
import {
    apiLevelLog
} from "./api/level_log";
import {
    levelSessionStorage
} from "./session_storage";

async function setPlayingOrder({
    levelId
}) {

    let res = await apiLevel.getSpecificLevel({
        levelId: levelId
    });

    if (!(res["auth"]["status"] && res["payload"]["status"])) {
        console.log("err");
        return;
    }

    let capacity = res["payload"]["capacity"]

    levelSessionStorage.setCapacity({
        capacity: capacity
    });

    let joinToUsername = {}

    for (const value of Object.values(res["payload"]["users"])) {
        joinToUsername[value.joinId] = {
            username: value.username,
        };
    }

    res = await apiLevelLog.getLevelLog(levelId);

    if (!(res["auth"]["status"] && res["payload"]["status"])) {
        console.log("err");
        return;
    }

    let log = res["payload"]["log"];

    // total count of people

    let order = {};
    let c = 0;

    for (const value of Object.values(log)) {

        if (value.action === "goes") {

            order[c] = {
                joinIndex: value.player,
                username: joinToUsername[value.player].username
            }
            c++;
        }

        if (capacity === c) {
            break
        }

    }

    if (capacity !== c) {
        console.log("err logical")
    }

    levelSessionStorage.setOrder({
        order: order
    });

    return order;

}

async function setJoinIndex(username, levelId) {
    let res = await apiLevel.getSpecificLevel({ levelId: levelId });

    if (!(res["auth"]["status"] && res["payload"]["status"])) {
      console.log("err");
      return;
    }

    for (const value of Object.values(res["payload"]["users"])) {
      if (value.username === username) {
        levelSessionStorage.set({
          variable: "JoinIndex",
          value: value.joinId,
        });

        return;
      }
    }
  }

export {
    setPlayingOrder,
    setJoinIndex
}