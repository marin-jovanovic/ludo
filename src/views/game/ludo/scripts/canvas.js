class Canvas {
    
    constructor(element) {
        this.canvas = element;
        this.canvas.width = 600;
        this.canvas.height = 600;
        // this.canvas.width = innerWidth;
        // this.canvas.height = innerHeight;

        this.context = this.canvas.getContext("2d");
        this.animationId;


        // this.canvas2 = element;
        // this.canvas2.width = 600;
        // this.canvas2.height = 600;
        // // this.canvas.width = innerWidth;
        // // this.canvas.height = innerHeight;

        // this.context2 = this.canvas2.getContext("2d");


        // this.animate = this.animate.bind(this);
    }

    clear = () => {

        // leave no trace
        this.context.clearRect(0, 0, this.canvas.width, this.canvas.height)

    }

    animateOnce = (args) => {
        // console.log(args)
        // console.log(args.level)
        this.clear();

        // board
        args.level.boardTiles.forEach((b) => {
            b.draw(this.context)
        })

        // // tokens
        // for (const p of Object.values(level.players)) {

        //     for (const t of Object.values(p.tokens)) {
        //         t.draw(canvas.context)
        //     }

        // }

    }




    animate = (notifArgs) => {

        let level = notifArgs.level;
console.log(level)

        // requestAnimationFrame((level) => {
        
        // });
// return
   
        // this.notify = this.notify.bind(this);

        let animateDriver = () => {

            // setup
            this.canvas.animationId = requestAnimationFrame(animateDriver)

            this.clear();

            level.boardTiles.forEach((b) => {
                b.draw(this.context)
            })

            // tokens
            Object.values(level.players).forEach(p => {

                Object.values(p.tokens).forEach(t => {
    
                    t.draw(this.context)
    
                });
        
            });
    
    
        }

        animateDriver();
    }

    animationLoop = (level) => {

        Object.values(level.players).forEach(p => {

            Object.values(p.tokens).forEach(t => {

                t.draw(this.context)

            });
    
        });

    }


}

class CanvasStatic extends Canvas {
    constructor(element) {
        super(element);
    }

    animateOnce = (args) => {
        // console.log(args)
        // console.log(args.level)
        this.clear();

        // board
        args.level.boardTiles.forEach((b) => {
            b.draw(this.context)
        })

        // // tokens
        // for (const p of Object.values(level.players)) {

        //     for (const t of Object.values(p.tokens)) {
        //         t.draw(canvas.context)
        //     }

        // }

    }
}

class CanvasReactive extends Canvas {

    constructor(element) {
        super(element);

    }

    animate(notifArgs) {
        // console.log("anim")

        console.log(notifArgs)
        // let canvas  = this.canvas;
        let level = notifArgs.level;


                // tokens
        for (const p of Object.values(level.players)) {

            for (const t of Object.values(p.tokens)) {
                t.draw(this.context)
            }

        }

        // // this.notify = this.notify.bind(this);

        // function animateDriver() {

        //     // setup
        //     canvas.animationId = requestAnimationFrame(animateDriver);

        //     // canvas.clear();
        //     // clear = () => {

        //         // leave no trace
        //         // canvas.context.clearRect(0, 0, canvas.width, canvas.height)
        
        //     // }
        //     // board
        //     // level.boundaries.forEach((b) => {
        //     //     b.draw(canvas.context)
        //     // })

        //     // // tokens
        //     for (const p of Object.values(level.players)) {

        //         for (const t of Object.values(p.tokens)) {
        //             t.draw(canvas.context)
        //         }

        //     }


        // }

        // animateDriver();
    }

}


export { 
    Canvas,
    CanvasStatic,
    CanvasReactive
}