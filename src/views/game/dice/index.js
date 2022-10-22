

function createCSSSelector(selector, style) {
    if (!document.styleSheets) return;
    if (document.getElementsByTagName('head').length == 0) return;

    let styleSheet, mediaType;

    if (document.styleSheets.length > 0) {
        for (let i = 0, l = document.styleSheets.length; i < l; i++) {
            if (document.styleSheets[i].disabled)
                continue;
            let media = document.styleSheets[i].media;
            mediaType = typeof media;

            if (mediaType === 'string') {
                if (media === '' || (media.indexOf('screen') !== -1)) {
                    styleSheet = document.styleSheets[i];
                }
            }
            else if (mediaType == 'object') {
                if (media.mediaText === '' || (media.mediaText.indexOf('screen') !== -1)) {
                    styleSheet = document.styleSheets[i];
                }
            }

            if (typeof styleSheet !== 'undefined')
                break;
        }
    }

    if (typeof styleSheet === 'undefined') {
        let styleSheetElement = document.createElement('style');
        styleSheetElement.type = 'text/css';
        document.getElementsByTagName('head')[0].appendChild(styleSheetElement);

        for (let i = 0; i < document.styleSheets.length; i++) {
            if (document.styleSheets[i].disabled) {
                continue;
            }
            styleSheet = document.styleSheets[i];
        }

        mediaType = typeof styleSheet.media;
    }

    if (mediaType === 'string') {
        for (let i = 0, l = styleSheet.rules.length; i < l; i++) {
            if (styleSheet.rules[i].selectorText && styleSheet.rules[i].selectorText.toLowerCase() == selector.toLowerCase()) {
                styleSheet.rules[i].style.cssText = style;
                return;
            }
        }
        styleSheet.addRule(selector, style);
    }
    else if (mediaType === 'object') {
        let styleSheetLength = (styleSheet.cssRules) ? styleSheet.cssRules.length : 0;
        for (let i = 0; i < styleSheetLength; i++) {
            if (styleSheet.cssRules[i].selectorText && styleSheet.cssRules[i].selectorText.toLowerCase() == selector.toLowerCase()) {
                styleSheet.cssRules[i].style.cssText = style;
                return;
            }
        }
        styleSheet.insertRule(selector + '{' + style + '}', styleSheetLength);
    }
}

function createDotsCSS() {
    let yCSSRules = {
        left: 20,
        right: 80,
        center: 50
    }

    let xCSSRules = {
        up: 20,
        down: 80,
        center: 50,
    }


    for (const [y, yRule] of Object.entries(yCSSRules)) {
        for (const [x, xRule] of Object.entries(xCSSRules)) {
            createCSSSelector('.' + x + '-' + y, 'left: ' + xRule + '%; top: ' + yRule + '%;')
        }
    }

}

function createDots(sides) {
    for (const [key, side] of Object.entries(sides)) {
        let dots = side.dots;
        let c = document.querySelector('#' + key)

        dots.forEach(i => {
            let d = document.createElement('div')
            d.classList.add('dot')
            d.classList.add(i)
            c.append(d)
        })


    }

}

function createSides(sides) {

    for (const [s, value] of Object.entries(sides)) {
        let c = document.querySelector('.dice');
        let d = document.createElement('div')
        d.classList.add('side')
        d.setAttribute("id", s);
        c.append(d);

        let style = 'transform: ';
        if (value.initRotation.x) {
            style += 'rotateX(' + value.initRotation.x + 'deg) ';
        }
        if (value.initRotation.y) {
            style += 'rotateY(' + value.initRotation.y + 'deg) ';
        }

        style += 'translateZ(3.1em)';
        createCSSSelector('#' + s, style)
    }

}

function getDiceConfig() {
    return {
        one: {
            dots: ['center-center'],
            rotations: {
                x: 0,
                y: 0
            },
            initRotation: {
                x: 0,
                y: 0
            }
        },
        two: {
            dots: ['up-left', 'down-right'],
            rotations: {
                x: -90,
                y: 0
            },
            initRotation: {
                x: 90,
                y: 0
            }

        },
        three: {
            dots: ['up-left', 'center-center', 'down-right'],
            rotations: {
                x: 0,
                y: 90
            },
            initRotation: {
                x: 0,
                y: -90
            }
        },
        four: {
            dots: ['up-left', 'up-right', 'down-left', 'down-right'],
            rotations: {
                x: 0,
                y: -90
            },
            initRotation: {
                x: 0,
                y: 90
            }
        },
        five: {
            dots: ['up-left', 'up-right', 'down-left', 'down-right', 'center-center'],
            rotations: {
                x: 90,
                y: 0
            },
            initRotation: {
                x: -90,
                y: 0
            }
        },
        six: {
            dots: ['up-left', 'up-right', 'down-left', 'down-right', 'center-left', 'center-right'],
            rotations: {
                x: 0,
                y: 180
            },
            initRotation: {
                x: 0,
                y: 180
            }
        },
    }

}




let currX = 0;
let currY = 0;

function rollDice(result) {


    function getTransformation(number) {
        let style = '';

        let numberToString = {
            1: 'one',
            2: 'two',
            3: 'three',
            4: 'four',
            5: 'five',
            6: 'six'
        }


        let dice = getDiceConfig()[numberToString[number]].rotations;

        let x, y;

        if (currX >= 0) {
            x = dice.x - 2 * 1440
        } else {
            x = dice.x + 2 * 1440
        }

        if (currY >= 0) {
            y = dice.y - 2 * 1440
        } else {
            y = dice.y + 2 * 1440
        }

        style += 'rotateX(' + x + 'deg) ';
        style += 'rotateY(' + y + 'deg)';
        // rotateZ

        currX += x
        currY += y

        return style
    }

    document.querySelector('.dice').style.transform = getTransformation(result)

}

function startup() {

    let dice = getDiceConfig();
    createSides(dice);

    createDots(dice);
    createDotsCSS();

}

export const dice = {
startup,
rollDice
}
