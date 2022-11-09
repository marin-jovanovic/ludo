
function addEventListenerToDocument(type, listener) {
    addEventListener(type, listener)
}

function removeEventListenerToDocument(type, listener) {
    removeEventListener(type, listener)
}

export const listeners = {
    addEventListenerToDocument,
    removeEventListenerToDocument
}