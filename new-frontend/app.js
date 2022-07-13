const signUpBtn = document.querySelector('#sign-up-btn');
const signInBtn = document.querySelector('#sign-in-btn');

signUpBtn.addEventListener('click', function(e) {
    e.preventDefault();
    window.location.href = "./sign-up/"
});

signInBtn.addEventListener('click', function(e) {
    e.preventDefault();
    window.location.href = "./sign-in/"
});