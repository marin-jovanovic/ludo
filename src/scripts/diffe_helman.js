


function f() {
    console.log("t")
}


(async () => {

    const Elliptic = require('elliptic').ec;
    const ec = new Elliptic('secp256k1');
    
    // Generate a private key for Alice
    const alice = ec.genKeyPair();
    
    // Generate a private key for Bob
    const bob = ec.genKeyPair();
    
    // Calculate the public key for Alice
    const alicePublicKey = alice.getPublic();
    
    // Calculate the public key for Bob
    const bobPublicKey = bob.getPublic();
    
    // Alice calculates the shared secret key
    const aliceSharedSecret = alice.derive(bobPublicKey);
    
    // Bob calculates the shared secret key
    const bobSharedSecret = bob.derive(alicePublicKey);
    
    console.log("Alice's shared secret:", aliceSharedSecret.toString(16));
    console.log("Bob's shared secret:", bobSharedSecret.toString(16));
    

})();

export {
    f
}