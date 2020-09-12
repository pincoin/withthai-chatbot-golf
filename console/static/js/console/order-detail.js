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
            const time = this.parentNode.parentNode.parentNode.children[1].children[0].children[0].children[0].value
            const div = document.createElement('div');
            div.innerHTML = '<div class="field has-addons action-field-centered mb-3">\n' +
                '<div class="control">\n' +
                '    <input class="input"\n' +
                '        type="time"\n' +
                '        value="' + time + '"\n' +
                '        name="tee_off_times"\n' +
                '        placeholder="HH:MM" step="60">\n' +
                '</div>\n' +
                '<div class="control">\n' +
                '    <a class="button is-danger offer-minus">\n' +
                '        <i class="fas fa-minus fa-fw"></i>\n' +
                '    </a>\n' +
                '</div>\n' +
                '</div>';
            while (div.children.length > 0) {
                div.children[0].children[1].children[0].addEventListener('click', function () {
                    this.parentElement.parentElement.remove();
                });

                offer_list.appendChild(div.children[0]);
            }
        });

    // Close Modal
    const closeModal = document.getElementById('close-modal');
    const closeModalBody = document.getElementById('close-modal-body');
    const closeModalCancel = document.getElementById('close-modal-cancel');
    const closeModalClose = document.getElementById('close-modal-close');

    document.getElementById('close-button').addEventListener('click', function (e) {
        if (!closeModal.classList.contains('is-active')) {
            closeModal.classList.add('is-active');
        }
    });

    [closeModalCancel, closeModalClose].forEach(function (element) {
        element.addEventListener('click', function (e) {
            if (closeModal.classList.contains('is-active')) {
                closeModal.classList.remove('is-active');
            }
        });
    });

    document.getElementById('close-modal-ok').addEventListener('click', function (e) {
        document.getElementById('reject-form').submit();
    });
}