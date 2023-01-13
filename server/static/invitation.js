const genLinkBtn = document.querySelector('#genLinkBtn');
const link = document.querySelector('#linkUrl');
const copyBtn = document.querySelector('#copyLinkBtn');

genLinkBtn.addEventListener('click', (e) => {
    e.preventDefault();
    copyLinkBtn.style.display = 'block';
    link.style.display = 'block';
    requestLink();
});

copyBtn.addEventListener('click', (e) => {
    e.preventDefault();
    link.select();
    document.execCommand('copy');
});

function requestLink() {
    fetch('', {
        method: 'POST',
    })
        .then(res => console.log(res))
        // .then(res => res.json())
        .then(data => {
            link.value = data.link;
        });
    console.log('request sent');
}
