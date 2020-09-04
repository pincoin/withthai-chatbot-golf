document.addEventListener('DOMContentLoaded', () => {
    document
        .getElementById('burger-icon')
        .addEventListener('click', function (e) {
            const left_sidebar = document.getElementById('left-sidebar');

            if (left_sidebar.classList.contains('is-hidden-mobile')) {
                left_sidebar.classList.remove('is-hidden-mobile');
            } else {
                left_sidebar.classList.add('is-hidden-mobile');
            }
        });

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
});