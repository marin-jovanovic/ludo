class WebSocketListener {
    constructor(url, onMessageAction) {

        self.socket = new WebSocket(url);


        self.socket.onopen = function() {
            console.log("[ws open] Connection established");
        };

        self.socket.onmessage = function(event) {
            console.log("[ws message]", event);

            // console.log(event.data, typeof(event.data))


            let message = JSON.parse(event.data);

            // console.log(message.message)

            onMessageAction(message);

            // if (message.message === "getUserActive") {
            //     console.log("ws get user active")

            //     console.log(message.args);
            //     // document.querySelector("#au").innerHTML = Object.keys(message.args)

            // } else {
            //     console.log("other msg")
            // }

        };

        self.socket.onclose = function(event) {
            if (event.wasClean) {
                console.log(`[ws close] Connection closed cleanly, code=${event.code} reason=${event.reason}`);
            } else {
                // e.g. server process killed or network down
                // event.code is usually 1006 in this case
                console.log('[ws close] Connection died');
            }
        };

        self.socket.onerror = function(error) {
            console.log("err", error)
            console.log(`[ws error] ${error.message}`);
        };

    }

    start() {
        console.log("start ws listenrs")
    }

    sendMessage(payload) {
        self.socket.send(payload)
    }

}

// function getUserActive(message) {
//     console.log("ws get user active")
//     console.log(message)            

//     // console.log(message.args);

// }


// let wsGetUserActive = new WebSocketListener(url, getUserActive);

export const wsListeners = {
    // createGame,
    // getGames,
    // leaveGame,
    // joinGame
    // wsGetUserActive,
    WebSocketListener

}