let socket = new WebSocket("ws://127.0.0.1:8000/ws");

socket.onopen = function(e) {
    console.log("[open] Connection established");   

    let username = document.querySelector("#u").value;
    let accessToken = document.querySelector("#at").value;

    let payload = {
        header: {
            username: username,
            accessToken: accessToken
        },
        payload: {
            command: "getActive",
            args: {
            }
        }
    }

    payload = JSON.stringify(payload)

    console.log("Sending to server");
    socket.send(payload)
};

socket.onmessage = function(event) {
    console.log(`[message] Data received from server: ${event.data}`);

    // let message = event.data;
    let message = JSON.parse(event.data);
    console.table(message)

    console.log(message.message)
    if (message.message === "getUserActive") {
        console.log("get user active")
        
        document.querySelector("#au").innerHTML = Object.keys(message.args)
    
    } else {
        console.log("other msg")
    }

};

socket.onclose = function(event) {
    if (event.wasClean) {
        console.log(`[close] Connection closed cleanly, code=${event.code} reason=${event.reason}`);
    } else {
        // e.g. server process killed or network down
        // event.code is usually 1006 in this case
        console.log('[close] Connection died');
    }
};

socket.onerror = function(error) {
    console.log(`[error] ${error.message}`);
};


document.querySelector("#li").addEventListener("click", e => {
    let username = document.querySelector("#u").value;
    let accessToken = document.querySelector("#at").value;

    let payload = {
        header: {
            username: username,
            accessToken: accessToken
        },
        payload: {
            command: "logIn",
            args: {
            }
        }
    }

    payload = JSON.stringify(payload)

    console.log("Sending to server");
    socket.send(payload)
})

document.querySelector("#c").addEventListener("click", e => {

    let username = document.querySelector("#u").value;
    let accessToken = document.querySelector("#at").value;

    let payload = {
        header: {
            username: username,
            accessToken: accessToken
        },
        payload: {
            command: "createRoom",
            args: {
                roomId: "room1",
                capacity: 4
            }
        }
    }

    payload = JSON.stringify(payload)

    console.log("Sending to server");
    socket.send(payload)

})