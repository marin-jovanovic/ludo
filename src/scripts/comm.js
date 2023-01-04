function sleep({ms}) {
    await new Promise((r) => setTimeout(r, ms));
}

export {
    sleep
}