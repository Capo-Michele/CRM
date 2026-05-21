const hamburger = document.querySelector('#toggle-button');

hamburger.addEventListener('click', function () {
    document.querySelector('#sidebar').classList.toggle('expand');
});