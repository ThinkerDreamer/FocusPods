# FocusPods

![focuspods-small](https://user-images.githubusercontent.com/74881094/212347374-f07b103f-490f-4bd7-b228-6345d3025cf9.png)

### A full-stack webapp created to share whether or not you are focusing with whoever you want


The backend is written in Python with the Flask framework and a Postgres database.
The frontend is currently pure HTML, CSS, and a little JavaScript, but I have plans to create a Svelte frontend in the future.

## Current functionality
Now you can:
- sign up
- log in
- create a "pod" (a group to share focus status)
- go to your pod

## Work-in-progress functionality
You will be able to:
- create a link to share with friends/coworkers so they can join your pod
- toggle your focus state and view the focus state of others in the pod

### Security
Please do not use any real personal information with this app, as there is not yet any app security implemented.
Passwords are not hashed, but rather saved plaintext in the Postgres database. Passwords will be hashed in the future.

![focuspods-login](https://user-images.githubusercontent.com/74881094/212348117-b680c3c9-4f25-4573-beb3-43d7f58d70a7.png)
