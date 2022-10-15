window.onload = () => {
    (async () => {
        await map_drivers();
    })();
}

var map_inst = SingletonFactory.getInstance();


function href_jump(h) {

    document.getElementById(h).scrollIntoView();
}


var SingletonFactory = (function () {
    class SingletonClass {

        constructor() {

        }


    }
    var instance;
    return {
        getInstance: function () {
            if (instance == null) {
                instance = new SingletonClass();
                instance.constructor = null;
            }
            return instance;
        }
    };
})();


