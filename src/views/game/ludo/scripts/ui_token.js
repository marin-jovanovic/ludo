import { ContentCreator } from "./content_creator.js";


/**
 * ===>>>
 * bl fires "bl token state updated"
 * bl sets flag that he sent info that something is updated
 * he will not fire another event until someone sends event back
 * 
 * this hints ui to update tokens position
 * 
 * <<<===
 * ui moves token to destination position
 * ui fires "ui token updated"
 * 
 * bl now knows that someone is listening
 * bl now knows that he can send another update/event 
 * 
 * -------------
 * bl has stack in which he keeps change log
 * when he can fire he will pop oldest change from stack and fire it
 * 
 * 
 */

class UiToken extends ContentCreator {

    constructor({ position, colour}) {
        super();

        // x, y
        this.position = position;
        // todo determine (if game mode all_at_same_place then you know) else one by one
        // what if second is faster then this first one, still undetermined, this must update depending which ends first 
        this.destinationPosition = position;

        this.radius = 8
        this.colour = colour;
        this.startingPosition = { x: position.x, y: position.y };

        // for jumping between tiles
        this.backlog = [];
        this.backlogSleepFrameCount = 10;
        this.backlogSleepFrameDec = 0;
        this.startSleeping = false;

        // todo extract to config
        // for jumping; sleep on each tile between start end destination tile
        // one by one
        this.configSleep = true;

        // move one by one tile (no diagonal => rather use first x then y ie)
        // prevent diagonals
        this.configOneByOne = true;


        this.choice_oneByOne_pythagoras = true;

    }

    restart = () => {
        /**
         * one enemy token eats this token; move it to start position
         */

        console.log("restart ui")

        this.setDestionationPosition({ 
            destinationPosition: this.startingPosition 
        })
 
    }

    setDestionationPosition = ({destinationPosition}) => {
        this.destinationPosition = destinationPosition;
    }

    // moveByOne = ({ destinationPosition }) => {
    //     console.log("move by one")

    //     this.setDestionationPosition(destinationPosition)
    // }


    _moveByOneToDestination = (des) => {
        let atNextDestination = true;

        ['x', 'y'].forEach(i => {
        
            if (this.position[i] !== des[i]) {
                atNextDestination = false;
        
                if (this.position[i] > des[i]) {
                    this.position[i]--;
                } else if (this.position[i] < des[i]) {
                    this.position[i]++;
                }

            }
        })

        return atNextDestination;
    }

    draw = (c) => {
        
        c.beginPath()
        c.arc(
            this.position.x,
            this.position.y,
            this.radius,
            0,
            Math.PI * 2,
        );

        this._moveByOneToDestination(this.destinationPosition);

        c.fillStyle = this.colour
        c.fill()
        c.closePath()
    }

}

export { UiToken }