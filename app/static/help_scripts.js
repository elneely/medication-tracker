/* This contains the JS for help.html */

const accordion = document.getElementsByClassName('help-section');

for (i=0; i<accordion.length; i++) {
    accordion[i].addEventListener('click', function() {
        this.classList.toggle('active')
    })
}