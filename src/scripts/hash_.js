
const generatePasswordHash = async (password) => {
    // Set the algorithm, salt and number of iterations
    const algorithm = "SHA-256";
    const salt = new TextEncoder().encode(Math.random().toString());
    const iterations = 100000;
    // Generate the password hash
    const key = await crypto.subtle.importKey(
        "raw",
        new TextEncoder().encode(password),
        {name: "PBKDF2"},
        false,
        ["deriveBits", "deriveKey"]
    );
    const passwordHash = await crypto.subtle.deriveBits(
        {
            name: "PBKDF2",
            salt,
            iterations,
            hash: algorithm
        },
        key,
        256
    );
    // Return the password hash and the salt
    return {passwordHash, salt};
}

// Function to verify password
const verifyPassword = async (password, passwordHash, salt) => {
    // Set the algorithm and number of iterations
    const algorithm = "SHA-256";
    const iterations = 100000;
    // Verify the password
    const key = await crypto.subtle.importKey(
        "raw",
        new TextEncoder().encode(password),
        {name: "PBKDF2"},
        false,
        ["deriveBits", "deriveKey"]
    );
    const newpasswordHash = await crypto.subtle.deriveBits(
        {
            name: "PBKDF2",
            salt,
            iterations,
            hash: algorithm
        },
        key,
        256
    );



let len = new Uint8Array(newpasswordHash).length
let n = new Uint8Array(newpasswordHash)
let o = new Uint8Array(passwordHash)
let isSame = true;
        for (let i = 0; i < len; i++) {
            console.log(n[i] == o[i])
            if (n[i]!== o[i]) {
                isSame = false;
            }

        }

console.log("is same", isSame)

        return isSame

        // new Uint8Array(newpasswordHash).forEach(i => {
        //     console.log(i, i===)
        // })

    // compare the passwordHash with the newpasswordHash
    // return passwordHash === newpasswordHash;
}


const generateHashWrapper = async (password) => {

    let {passwordHash, salt} = await generatePasswordHash(password);

    if (await verifyPassword(password, passwordHash, salt)) {
        return {
            status: true,
            passwordHash: passwordHash,
            salt: salt
        }
    } else {
        return{
            status: false
        }
    }

}

export {
    generateHashWrapper
}