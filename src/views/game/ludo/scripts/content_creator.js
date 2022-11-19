
class ContentCreator {

    constructor() {
        this.subscribers = {};
    }

    subscribe({command, s}) {

        console.log("subscribe", command, s)

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

        console.log("notif", command, args)
        // console.log(typeof(args))
        // console.log(...args)

        if (!(command in this.subscribers)) {
            console.log("unknown command")
            return
        }

        this.subscribers[command].forEach((i) => {
            i(args);
        });
    }

}

export {
    ContentCreator
}