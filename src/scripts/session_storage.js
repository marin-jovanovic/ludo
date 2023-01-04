class SessionStorageWrapper {
    constructor() {
        this.vals = new Set([
            'username',
            'accessToken',
            'profilePhoto',
            'levelId',

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


        sessionStorage.setItem(variable, value);

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



        // console.log(sessionStorage.getItem(variable));

        return {
            status: true,
            payload: sessionStorage.getItem(variable)
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
            }).payload
        }
    }
}




class LevelSS {
    constructor() {
        this.ssw = new SessionStorageWrapper();
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

    leaveLevel() {
        if (!

            this.ssw.remove({
                variable: "levelId"
            }) 

        ) {
            console.log("err removing")
        }

    }
 
    // is in any level

    getLevelMeta() {
        return {
            levelId: this.ssw.get({
                variable: "levelId"
            }).payload,
        }
    }
}


let userMetaSS = new UserMetaSS();
let levelSessionStorage = new LevelSS();

export {
    userMetaSS,
    levelSessionStorage
}