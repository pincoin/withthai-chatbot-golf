function runApp() {
    const confirm_form = document.getElementById('confirm-form');
    const offer_form = document.getElementById('offer-form');
    const reject_form = document.getElementById('reject-form');

    const offer_list = document.getElementById('offer-list');

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

    document
        .getElementById('offer-plus')
        .addEventListener('click', function (e) {
            const div = document.createElement('div');
            div.innerHTML = '<div class="field has-addons action-field-centered">\n' +
                '<p class="control">\n' +
                '    <input class="input"\n' +
                '        type="time"\n' +
                '        name="tee_off_times"\n' +
                '        placeholder="HH:MM" step="60">\n' +
                '</p>\n' +
                '<p class="control">\n' +
                '    <a class="button is-danger offer-minus">\n' +
                '        <i class="fas fa-minus fa-fw"></i>\n' +
                '    </a>\n' +
                '</p>\n' +
                '</div>';
            while (div.children.length > 0) {
                div.children[0].children[1].children[0].addEventListener('click', function () {
                    this.parentElement.parentElement.remove();
                });

                offer_list.appendChild(div.children[0]);
            }
        });
}