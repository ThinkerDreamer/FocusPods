/* 
have pods (groups of users who want to share their focus state with each other)
 --HTML element for sharing
 --redirect
 --first only ppl w/acct

 -- BACK BURNER in each pod, each user has a to-do list
 
there's a button to flip between focusing and not
each user in the pod can see everyone else in the pod's focus state and to-do list

each pod has its own unique URL
-- login (firebase authz and auth)
-- make unique URLs
*/


console.log("pre-import");
//Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/9.6.6/firebase-app.js";
import { child, get, getDatabase, onValue, ref, set } from "https://www.gstatic.com/firebasejs/9.6.6/firebase-database.js";
// import {getAuth, createUserWithEmailAndPassword} from "https://www.gstatic.com/firebasejs/9.6.6/firebase-auth.js";
console.log("done importing FireBase Database")

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
    apiKey: "AIzaSyBnLC8Z-kY_9D-c2haaeqFlZEJyF-6krkM",
    authDomain: "focus-button.firebaseapp.com",
    databaseURL: "https://focus-button-default-rtdb.europe-west1.firebasedatabase.app",
    projectId: "focus-button",
    storageBucket: "focus-button.appspot.com",
    messagingSenderId: "1022607046698",
    appId: "1:1022607046698:web:d925f9e5e484d580dfab53",
    measurementId: "G-HL8BDEHKJK"
};

// Initialize Firebase
const firebaseApp = initializeApp(firebaseConfig);
// Get a reference to the database service
const database = getDatabase(firebaseApp, firebaseConfig.databaseURL);
// const auth = getAuth();

console.log("done initializing Firebase");

// My personal functions
function writeData(person, focusParam) {
    //alert(`value of focusParam: ${focusParam}`);
    if (focusParam) {
        //console.log(`focusParam is (true) ${focusParam}, now making it false`);
        set(ref(database, `${person}`), {
            focusing: false
        })
    } else if (!focusParam) {
        //console.log(`focusParam is (false) ${focusParam}, now making it true`);
        set(ref(database, `${person}`), {
            focusing: true
        })
    } else {
        alert("focusParam is neither true nor false: " + focusParam);
    }
}
function getData(person) {
    const dbref = ref(database);
    get(child(dbref, `/${person}`)).then((snapshot) => {
        if (snapshot.exists()) {
            let focusValue = snapshot.val()["focusing"];
            writeData(person, focusValue);
            //alert(`snapshot exists, focusValue = ${focusValue}, person = ${person}`);
        } else {
            alert("No data found");
        }
    })
        .catch((error) => {
            //alert(`getData error, focusValue = ${focusValue}`);
            alert("Unsuccessful. Error: " + error);
        })
}
function readValue(person) {
    const dbref = ref(database);
    onValue(child(dbref, `/${person}/focusing`), (snapshot) => {
        const changed = snapshot.val();
        //alert(`changed ${changed}`);
        updateDom(changed, person);
        const queryString = window.location.search;
        const urlParams = new URLSearchParams(queryString);
        const name = urlParams.get('name');
        console.log(name);
        //alertIfFocused(name);
    });
}
function updateDom(changed, person) {
    if (changed) {
        document.querySelector(`#${person}State`).innerText = "Focusing";
    } else {
        document.querySelector(`#${person}State`).innerText = "Not focusing";
    }
}

function getFocusState(name) {
    const dbref = ref(database);
    return onValue(child(dbref, `/${name}/focusing`), (snapshot) => {
        return snapshot.val()
    });
}

function alertIfFocused(name) {
    //console.log("alertIfFocused was called and name=", name);
    if (getFocusState(name)) {
        //console.log("alertIfFocused was triggered and person is not focused");
        if (name === 'angel' && getFocusState('luca')) {
            alert("Luca is now focusing.");
        }
    } else if (name === 'luca') {
        if (getFocusState('angel')) {
            alert("Angel is now focusing.");
        }
    } else {
        //console.log("alertIfFocused was called but getFocusState was false");
    }
}
const themeButton = document.querySelector("#themeButton");
const modes = {
    dark: "Dark",
    pastel: "Pastel"
}

let currentMode = modes.pastel;

themeButton.addEventListener("click", function () {
    themeButton.textContent = `${currentMode} mode`;
    currentMode = (themeButton.textContent === `Dark mode`)
        ? modes.pastel
        : modes.dark;
    const backgroundColor = `var(--${currentMode}-rainbow-gradient)`;
    document.body.style.setProperty("--background-gradient", backgroundColor);
    const mainEl = document.querySelector("main");
    if (currentMode === "Dark") {
        mainEl.style.background = "var(--Dark-mode-gradient)";
        console.log("Dark mode enabled");
    } else {
        mainEl.style.background = "var(--Blue-green-gradient)";
        console.log("Pastel mode enabled");
    }


    // if (currentMode === modes.bright) {
    //     console.log("Bright mode, setting button background color");
    //     document.querySelector("button").style.backgroundColor= "var(--Pastel-background-gradient-flipped)";
    // }
});
// const signUpButton = document.querySelector("#signUp");

// signUpButton.addEventListener("click", function () {
//     alert("signUpButton clicked");

//     let email = document.querySelector("#email").value;
//     let password = document.querySelector("#password").value;
//     let name = document.querySelector("#name").value;

//     createUserWithEmailAndPassword(auth, email, password)
//         .then((userCredential) => {
//             // Signed in
//             const user = userCredential.user;
//             set(ref(database, "users/" + user.uid),{
//                 email: email,
//                 name: name
//             })
//             alert("user created");
//             // ...
//         })
//         .catch((error) => {
//             const errorCode = error.code;
//             const errorMessage = error.message;
//             alert(errorMessage);
//             // ..
//         });
// })

readValue("luca");
readValue("angel");
const angelButton = document.querySelector("#angelButton");
const lucaButton = document.querySelector("#lucaButton");
angelButton.addEventListener("click", function () { getData("angel") });
lucaButton.addEventListener("click", function () { getData("luca") });