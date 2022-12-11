onChange() {

    console.log("on change")

    this.backlog.shift();

    if (this.backlog.length === 0) {
      return;
    }

    let first = this.backlog[0];

    // todo fix, add param for action, or multiple queues
    if (first.length === 2) {
      this.moveTokenToStart({ player: first[0], token: first[1] });
    } else {
      this.movePosition({
        player: first[0],
        token: first[1],
        jumpCount: first[2],
      });
    }
}

move token() {
            // if (this.useBacklog) {
        //     if (this.backlog.length === 0) {
        //       this.__movePositionDriver({
        //         player: player,
        //         token: token,
        //         jumpCount: jumpCount,
        //       });
        //     }
    
        //     this.backlog.push([player, token, jumpCount]);
        
        // } else {
        //     this.__movePositionDriver({
        //       player: player,
        //       token: token,
        //       jumpCount: jumpCount,
        //     });
        // }


                // this.__movePositionDriver({
        // player: notifArgs.player,
        // token: notifArgs.token,
        // jumpCount: notifArgs.jumpCount,
        // });

        // if (this.useBacklog) {
        //     if (this.backlog.length === 0) {
        //       this.__movePositionDriver({
        //         player: player,
        //         token: token,
        //         jumpCount: jumpCount,
        //       });
        //     }
    
        //     this.backlog.push([player, token, jumpCount]);
        
        // } else {
        //     this.__movePositionDriver({
        //       player: player,
        //       token: token,
        //       jumpCount: jumpCount,
        //     });
        // }

}

moveTokenToStart({ player, token }) {

    // if (this.useBacklog) {
    //     if (this.backlog.length === 0) {
    //       this.__restartToken({ player: player, token: token });
    //     }

    //     this.backlog.push([player, token]);
    // } else {
    //     this.__restartToken({ player: player, token: token });
    // }

}