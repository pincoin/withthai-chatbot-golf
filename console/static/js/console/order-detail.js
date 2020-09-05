function runApp() {
    const confirm_form = document.getElementById('confirm-form');
    const offer_form = document.getElementById('offer-form');
    const reject_form = document.getElementById('reject-form');

    document
        .getElementById('confirm-radio')
        .addEventListener('click', function (e) {
            confirm_form.classList.remove('is-hidden');
            offer_form.classList.add('is-hidden');
            reject_form.classList.add('is-hidden');
        });

    document
        .getElementById('offer-radio')
        .addEventListener('click', function (e) {
            confirm_form.classList.add('is-hidden');
            offer_form.classList.remove('is-hidden');
            reject_form.classList.add('is-hidden');
        });

    document
        .getElementById('reject-radio')
        .addEventListener('click', function (e) {
            confirm_form.classList.add('is-hidden');
            offer_form.classList.add('is-hidden');
            reject_form.classList.remove('is-hidden');
        });

    const offer_plus = document.getElementsByClassName('offer-plus');
    const offer_minus = document.getElementsByClassName('offer-minus');

    for (let i = 0; i < offer_plus.length; i++) {
        offer_plus[i].addEventListener("click", function () {
            console.log("Clicked index: " + i);
        })
    }

    for (let i = 0; i < offer_minus.length; i++) {
        offer_minus[i].addEventListener("click", function () {
            console.log("Clicked index: " + i);
        })
    }
}