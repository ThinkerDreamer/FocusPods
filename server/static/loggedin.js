const makeNewPodEl = document.querySelector('#makeNewPodEl');
const podName = document.querySelector('#podName');
const newPodSubmit = document.querySelector('#newPodSubmit');

makeNewPodEl.addEventListener('click', function (e) {
    e.preventDefault();
    podName.style.display = "block";
    newPodSubmit.style.display = "block"
})