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
            div.innerHTML = '<div class="field has-addons action-field-centered">\n' +
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

    // Confirm Modal
    const confirmModal = document.getElementById('confirm-modal');
    const confirmModalCancel = document.getElementById('confirm-modal-cancel');
    const confirmModalClose = document.getElementById('confirm-modal-close');
    const confirmModalRoundTime = document.getElementById('confirm-modal-round-time');

    const roundTime = document.getElementById('id_round_time');

    document.getElementById('confirm-button').addEventListener('click', function (e) {
        if (!confirmModal.classList.contains('is-active')) {
            confirmModal.classList.add('is-active');
        }

        confirmModalRoundTime.textContent = roundTime.value;
    });

    [confirmModalCancel, confirmModalClose].forEach(function (element) {
        element.addEventListener('click', function (e) {
            if (confirmModal.classList.contains('is-active')) {
                confirmModal.classList.remove('is-active');
            }
        });
    });

    document.getElementById('confirm-modal-ok').addEventListener('click', function (e) {
        document.getElementById('confirm-form').submit();
    });

    // Offer Modal
    const offerModal = document.getElementById('offer-modal');
    const offerModalCancel = document.getElementById('offer-modal-cancel');
    const offerModalClose = document.getElementById('offer-modal-close');
    const offerModalRoundTime = document.getElementById('offer-modal-round-time');

    document.getElementById('offer-button').addEventListener('click', function (e) {
        if (!offerModal.classList.contains('is-active')) {
            offerModal.classList.add('is-active');
        }

        offerModalRoundTime.textContent = '['
            + Array.from(document.getElementsByName('tee_off_times')).map(e => e.value).join(', ')
            + ']';
    });

    [offerModalCancel, offerModalClose].forEach(function (element) {
        element.addEventListener('click', function (e) {
            if (offerModal.classList.contains('is-active')) {
                offerModal.classList.remove('is-active');
            }
        });
    });

    document.getElementById('offer-modal-ok').addEventListener('click', function (e) {
        document.getElementById('offer-form').submit();
    });

    // Close Modal
    const closeModal = document.getElementById('close-modal');
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

    document.addEventListener('keyup', function (e) {
        let key = e.key || e.keyCode;

        if (key === 'Escape' || key === 'Esc' || key === 27) {
            if (confirmModal.classList.contains('is-active')) {
                confirmModal.classList.remove('is-active');
            }

            if (offerModal.classList.contains('is-active')) {
                offerModal.classList.remove('is-active');
            }

            if (closeModal.classList.contains('is-active')) {
                closeModal.classList.remove('is-active');
            }
        }
    });
}