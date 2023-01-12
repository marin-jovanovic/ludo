function isJsonString(str) {
    try {
        JSON.parse(str);
    } catch (e) {
        return false;
    }
    return true;
}



class SessionStorageWrapper {
    constructor() {

        // match by regex order | Order -> levelOrder

        this.vals = new Set([

            'userProfilePhoto',
            'username',
            'accessToken',

            'levelId',
            'levelOrder',
            'levelCapacity',
            "levelJoinIndex",

            "music",
        ])
    }

    isVariableLegal({
        variable
    }) {
        if (!this.vals.has(variable)) {
            console.log(`[err] ${variable} not accepted, if you need it add it to acceptable values`)
            return false;
        }

        return true;
    }

    isVariablePresent({
        variable
    }) {
        if (!this.vals.has(variable)) {
            console.log(`[err] ${variable} not accepted, if you need it add it to acceptable values`)
            return false;
        }

        return sessionStorage.getItem(variable) !== null;

    }

    set({
        variable,
        value
    }) {
        if (!this.isVariableLegal({
                variable: variable
            })) {
            return false;
        }

        if (value === undefined) {
            console.log("err, assumption that this was not intended")
            return
        }

        if (
            typeof value === 'object' &&
            !Array.isArray(value) &&
            value !== null
        ) {


            sessionStorage.setItem(variable, JSON.stringify(
                value
            ));

        } else {

            sessionStorage.setItem(variable, value);

        }



        return true;
    }

    get({
        variable
    }) {
        if (!this.isVariableLegal({
                variable: variable
            })) {
            return {
                status: false
            };
        }

        if (!this.isVariablePresent({
                variable: variable
            })) {
            console.log("err variable not present", variable)
            return {
                status: false
            };

        }

        let item = sessionStorage.getItem(variable);

        let parsed = undefined;

        if (isJsonString(item)) {

            parsed = JSON.parse(item);

        } else {

            parsed = item;

        }



        return {
            status: true,
            payload: parsed
        };
    }

    remove({
        variable
    }) {

        if (!this.isVariableLegal({
                variable: variable
            })) {
            return false;
        }

        sessionStorage.removeItem(variable);

        return true;
    }
}


class UserMetaSS {
    constructor() {
        this.ssw = new SessionStorageWrapper();
    }


    updateSettings({
        changes
    }) {

        for (const [key, value] of Object.entries(changes)) {
            console.log("updating", key, value)

            if (!
                this.ssw.set({
                    variable: key,
                    value: value
                })
            ) {
                console.log("err setting")
            }


        }

    }

    login({
        username,
        accessToken
    }) {
        this.username = username;
        this.accessToken = accessToken;

        if (!
            this.ssw.set({
                variable: "username",
                value: this.username
            })
        ) {
            console.log("err setting")
        }
        if (!
            this.ssw.set({
                variable: "accessToken",
                value: this.accessToken
            })
        ) {
            console.log("err setting");
        }
    }

    logout() {

        if (!

            this.ssw.remove({
                variable: "username"
            }) &&
            this.ssw.remove({
                variable: "accessToken"
            })

        ) {
            console.log("err removing")
        }
    }

    isAuth() {


        return this.ssw.get({
                variable: "username"
            }).status &&
            this.ssw.get({
                variable: "accessToken"
            }).status;

    }

    getCredentials() {
        return {
            username: this.ssw.get({
                variable: "username"
            }).payload,
            accessToken: this.ssw.get({
                variable: "accessToken"
            }).payload,

        }
    }


    getUserMeta() {

        // todo rewrite with level prefix


        return {
            userProfilePhoto: this.ssw.get({
                variable: "userProfilePhoto"
            }).payload,



            // levelId: this.ssw.get({
            //     variable: this.prefix + "Id"
            // }).payload,

            // // order: this.ssw.get({
            // //     variable: this.prefix + "Order"
            // // }).payload,
            // capacity: this.ssw.get({
            //     variable: this.prefix + "Capacity"
            // }).payload,

            // levelJoinIndex: this.ssw.get({
            //     variable: this.prefix + "JoinIndex"
            // }).payload,

        }
    }
}

class LevelSS {
    constructor() {
        this.ssw = new SessionStorageWrapper();

        this.prefix = "level";
    }

    joinLevel({
        levelId
    }) {

        console.log("--------- setting", levelId)

        this.levelId = levelId;

        if (!
            this.ssw.set({
                variable: "levelId",
                value: this.levelId
            })
        ) {
            console.log("err setting")
        }
    }

    set({
        variable,
        value
    }) {
        // joinId

        if (!
            this.ssw.set({
                variable: "level" + variable,
                value: value
            })
        ) {
            console.log("err setting", variable, value)
        }


    }



    leaveLevel() {
        if (!(

                this.ssw.remove({
                    variable: "levelId"
                }) &&

                this.ssw.remove({
                    variable: "levelOrder"
                }) &&

                this.ssw.remove({
                    variable: "levelCapacity"
                }) &&

                this.ssw.remove({
                    variable: "levelJoinIndex"
                })

            )


        ) {
            console.log("err removing")
        }

    }

    // is in any level

    getOrder() {
        return {

            order: this.ssw.get({
                variable: this.prefix + "Order"
            }).payload,

        }

    }

    getLevelMeta() {

        // todo rewrite with level prefix


        return {
            levelId: this.ssw.get({
                variable: this.prefix + "Id"
            }).payload,

            // order: this.ssw.get({
            //     variable: this.prefix + "Order"
            // }).payload,
            capacity: this.ssw.get({
                variable: this.prefix + "Capacity"
            }).payload,

            levelJoinIndex: this.ssw.get({
                variable: this.prefix + "JoinIndex"
            }).payload,

        }
    }
}


// class MusicSS {
//     constructor() {
//         this.ssw = new SessionStorageWrapper();
//     }

//     set({
//         value
//     }) {
//         // joinId

//         if (!
//             this.ssw.set({
//                 variable: "music",
//                 value: value
//             })
//         ) {
//             console.log("err setting", value)
//         }


//     }

//     get() {
//         return {

//             order: this.ssw.get({
//                 variable: "music"
//             }).payload,

//         }

//     }

// }

let userMetaSS = new UserMetaSS();
let levelSessionStorage = new LevelSS();

// let musicSS = new MusicSS();

export {
    userMetaSS,
    levelSessionStorage,
    // musicSS
}