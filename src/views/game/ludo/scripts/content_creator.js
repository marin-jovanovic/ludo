
class ContentCreator {
    /**
     * can create content
     * when creates something that subrscribers are subscribed to
     * can fire @notify 
     */

    constructor() {
        // console.log("created")
        this.subscribers = {};
    }

    subscribe({command, s}) {

        // console.log("subscribe", command, s)

        if (command in this.subscribers) {

            this.subscribers[command].add(s);

        } else {
            this.subscribers[command] = new Set();
            this.subscribers[command].add(s);
        }

    }

    unsubscribe({command, s}) {
        this.subscribers[command].delete(s);
    }

    notify({command, ...args}) {

        // console.log("notif", command, args)

        if (!(command in this.subscribers)) {
            console.log("no subscribers for this command");
            return;
        }

        // if (this.subscribers[command]) {

        //     console.log("can call")
        // }else {
        //     console.log("no function to call")
        // }

        // if (i in this.subscribers[command]) {

        // }

        // console.log(command)
        // console.log(
        //     this.subscribers[command]    
        // )

        this.subscribers[command].forEach((i) => {
            i(args);
        });
    }

}

export {
    ContentCreator
}