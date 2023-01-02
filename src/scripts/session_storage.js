class SessionStorageWrapper {
    constructor() {
        this.vals = new Set([
            'username',
            'accessToken',
            'profilePhoto',
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

    }

    login({
        username,
        accessToken
    }) {
        this.username = username;
        this.accessToken = accessToken;

        if (!
            ssw.set({
                variable: "username",
                value: this.username
            })
        ) {
            console.log("err setting")
        }
        if (!
            ssw.set({
                variable: "accessToken",
                value: this.accessToken
            })
        ) {
            console.log("err setting");
        }
    }

    logout() {

        if (!

            ssw.remove({
                variable: "username"
            }) &&
            ssw.remove({
                variable: "accessToken"
            })

        ) {
            console.log("err removing")
        }
    }

    isAuth() {


        return ssw.get({
            variable: "username"
        }).status && ssw.get({
            variable: "accessToken"
        }).status;

    }

    getCredentials() {
        return {
            username: ssw.get({
                variable: "username"
            }).payload,
            accessToken: ssw.get({
                variable: "accessToken"
            }).payload
        }
    }
}

let ssw = new SessionStorageWrapper();
let userMetaSS = new UserMetaSS();

export {
    ssw,
    userMetaSS
}