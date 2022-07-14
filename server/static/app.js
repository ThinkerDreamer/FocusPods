const signUpBtn = document.querySelector('#sign-up-btn');
const loginBtn = document.querySelector('#login-btn');

signUpBtn.addEventListener('click', function (e) {
    e.preventDefault();
    window.location.href = "/sign-up/"
});

loginBtn.addEventListener('click', function (e) {
    e.preventDefault();
    window.location.href = "/login/"
});