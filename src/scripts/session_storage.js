class SessionStorageWrapper {
    constructor() {
        this.vals = new Set([
            'username',
            'accessToken',
            'profilePhoto',
        ])
    }

    _test({variable}) {
        if (!this.vals.has(variable)) {
            console.log(`[err] ${variable} not accepted, if you need it add it to acceptable values`)
            return false;
        }

        return true;
    }

    set({variable, value}) {
        if (!this._test({variable: variable})) {
            return
        }
        sessionStorage.setItem(variable, value);
    }

    get({variable}) {
        if (!this._test({variable: variable})) {
            return
        }

        return sessionStorage.getItem(variable);
    }

    remove({variable}) {

        if (!this._test({variable: variable})) {
            return
        }

        return sessionStorage.removeItem(variable);
    }
}


class UserMetaSS {
    constructor() {

    }

    login({username, accessToken}) {
        this.username = username;
        this.accessToken = accessToken;

        ssw.set({variable: "username", value: this.username});
        ssw.set({variable: "accessToken", value: this.accessToken});
    }

    logout() { 

        ssw.remove({variable: "username"});
        ssw.remove({variable: "accessToken"});
    }

    isAuth() {

        return ssw.get({variable: "username"}) && ssw.get({variable: "accessToken"})
    }

    getCredentials() {
        return {
            username:  ssw.get({variable: "username"}),
            accessToken:  ssw.get({variable: "accessToken"})
        }
    }
}

let ssw = new SessionStorageWrapper();
let userMetaSS = new UserMetaSS();

export {
    ssw,
    userMetaSS
}
