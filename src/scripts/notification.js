import { useToast } from "vue-toastification";


class Notification {
    constructor() {
        this.toast = useToast();
    }

    showMessage = (result, successMessage, errorMessage) => {
        if (result) {
            if (successMessage) {
                this.toast.success(successMessage, {
                    timeout: 2000,
                });
            }
        } else {
            if (errorMessage) {
                this.toast.error(errorMessage, {
                    timeout: 2000,
                });
            }
        }
    }
    

}

let notification = new Notification();


export {
    notification
}


