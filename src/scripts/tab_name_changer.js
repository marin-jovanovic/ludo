// function getRandomNumber(min, max) {
//     return Math.floor(Math.random() * (max - min)) + min;
// }

const appName = "beyond";

function setIntervalDriver(params) {
    return setInterval(function () {
        if (params["titles"].length === params["index"]) {
            params["index"] = 0;
        }
        document.title = params["titles"][params["index"]];
        params["index"]++;
    }, params["countdown"]);

}

function visibleDefaultHiddenCustom(
    visible,
    hidden
){

    let hiddenDriver = null;

    document.addEventListener("visibilitychange", function () {

        if (document.hidden) {
            // clearInterval(visibleDriver);

            hiddenDriver = setIntervalDriver(
                hidden
            )

        } else {

            clearInterval(hiddenDriver);
            document.title = visible;

            // visibleDriver = setIntervalDriver(
            //     visible
            // )

        }

    });

}


// function tabChangedDriver(
//     visible,
//     hidden
// ) {

//     let visibleDriver = setIntervalDriver(
//         visible)

//     let hiddenDriver = null;

//     document.addEventListener("visibilitychange", function () {

//         if (document.hidden) {
//             clearInterval(visibleDriver);

//             hiddenDriver = setIntervalDriver(
//                 hidden
//             )

//         } else {

//             clearInterval(hiddenDriver);

//             visibleDriver = setIntervalDriver(
//                 visible
//             )

//         }

//     });

// }

// function shuffle(prev, wordArray) {

//     if (!wordArray.includes(prev)) {
//         throw "previous title not in array"
//     }

//     if (wordArray.length === 1) {
//         throw "only one element in array, previous title will always be equal current"
//     }

//     shuffleDriver(wordArray);

//     fixFirstElement(wordArray, prev);

//     return wordArray;

// }

// function shuffleDriver(wordArray) {
//     let currentIndex = wordArray.length, randomIndex;

//     while (currentIndex != 0) {

//         randomIndex = Math.floor(Math.random() * currentIndex);
//         currentIndex--;

//         [wordArray[currentIndex], wordArray[randomIndex]] = [
//             wordArray[randomIndex], wordArray[currentIndex]
//         ];
//     }
// }

// function fixFirstElement(wordArray, prev) {
//     let firstIndex = 0;

//     while (wordArray[firstIndex] === prev) {
//         // swap first element
//         let otherIndex = Math.floor(Math.random() * wordArray.length);
//         let temp = wordArray[firstIndex];
//         wordArray[firstIndex] = wordArray[otherIndex];
//         wordArray[otherIndex] = temp;
//     }
// }

// function oneUp(word) {

//     return Array(word.length).fill(word.toLowerCase()).map((e, i) => {
//         return e.slice(0, i) + e.charAt(i).toUpperCase() + e.slice(i + 1)
//     });

// }

// function oneDown(word) {

//     return Array(word.length).fill(word.toUpperCase()).map((e, i) => {
//         return e.slice(0, i) + e.charAt(i).toLowerCase() + e.slice(i + 1)
//     });

// }

function letters(word) {
    return word.split("");
}

export const activate_tab_name_changer = () => {

    // let visibleTitles = oneDown(appName)
    // visibleTitles.push(...oneUp(appName));

    let hiddenTitles = letters(appName);

    // let visibleCountdown = 1000;
    let hiddenCountdown = 200;

    onload = () => {

        // let visible = {
        //     "index": 0,
        //     "titles": visibleTitles,
        //     "countdown": visibleCountdown
        // };

        let hidden = {
            "index": 0,
            "titles": hiddenTitles,
            "countdown": hiddenCountdown
        };

        visibleDefaultHiddenCustom("Beyond", hidden)


        // tabChangedDriver(
        //     visible,
        //     hidden

        // );
    };

}