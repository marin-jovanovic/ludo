
class ActiveUsersSocket {
    constructor() {

        self.socket = new WebSocket("ws://127.0.0.1:8000/whole1/");

        self.activeUsers = {};
        
        self.socket.onopen = function(e) {
            console.log("active users");
            console.log("[open] Connection established");   
        };
        
        self.socket.onmessage = function(event) {
            console.log(event.data, typeof(event.data))


            let message = JSON.parse(event.data);
            // message = JSON.parse(message);

            console.log(message.message)
            if (message.message === "getUserActive") {
                console.log("get user active")
                
                document.querySelector("#au").innerHTML = Object.keys(message.args)
           
            } else {
                console.log("other msg")
            }
        
        };
        
        self.socket.onclose = function(event) {
            if (event.wasClean) {
                console.log(`[close] Connection closed cleanly, code=${event.code} reason=${event.reason}`);
            } else {
                // e.g. server process killed or network down
                // event.code is usually 1006 in this case
                console.log('[close] Connection died');
            }
        };
        
        self.socket.onerror = function(error) {
            console.log("err", error)
            console.log(`[error] ${error.message}`);
        };
        
    }

    sendMessage(payload) {
        self.socket.send(payload)
    }

}

let activeUsersSocket = new ActiveUsersSocket();

function fetchActiveUsers() {
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
    activeUsersSocket.sendMessage(payload)    
    
}


document.querySelector("#li").addEventListener("click", () => {

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
    // socket.send(payload)
    activeUsersSocket.sendMessage(payload)
})

