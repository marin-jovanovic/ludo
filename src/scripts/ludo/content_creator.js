class ContentCreator {
    /**
     * can create content
     * when creates something that subrscribers are subscribed to
     * can fire @notify 
     */

    constructor() {
        this.subscribers = {};
    }

    subscribe({
        command,
        s
    }) {

        if (command in this.subscribers) {
            this.subscribers[command].add(s);
        } else {
            this.subscribers[command] = new Set();
            this.subscribers[command].add(s);
        }

    }

    unsubscribe({
        command,
        s
    }) {
        this.subscribers[command].delete(s);
    }

    notify({
        command,
        ...args
    }) {

        if (!(command in this.subscribers)) {
            console.log("no subscribers for this command");
            return;
        }

        this.subscribers[command].forEach((i) => {
            i(args);
        });
    }

}

export {
    ContentCreator
}