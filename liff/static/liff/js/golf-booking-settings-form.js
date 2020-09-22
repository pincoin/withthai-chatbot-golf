const errorModal = document.getElementById('error-modal');
const errorModalTitle = document.getElementById('error-modal-title');
const errorModalBody = document.getElementById('error-modal-body');

function validateFullname(fullname, errorNotification) {
    return true;
}

function validateEmail(email, errorNotification) {
    return true;
}

function validatePhone(phone, errorNotification) {
    return true;
}

function validateLang(lang, errorNotification) {
    return true;
}

function validateForm(fullname, email, phone, lang, errorNotification) {
    if (!validateFullname(fullname, errorNotification)) {
        return false;
    }
    if (!validateEmail(email, errorNotification)) {
        return false;
    }
    if (!validatePhone(phone, errorNotification)) {
        return false;
    }
    return validateLang(lang, errorNotification);
}

function runApp() {
    // 1. Declares variables
    const fullname = document.getElementById('id_fullname');
    const email = document.getElementById('id_email');
    const phone = document.getElementById('id_phone');
    const lang = document.getElementById('id_lang');

    const bookingConfirmModal = document.getElementById('booking-confirm-modal');
    const modalTitle = document.getElementById('modal-title');
    const modalBody = document.getElementById('modal-body');

    const errorNotification = document.getElementById('error-notification');

    // 2. Retrieve customer group from server using access token
    /*
    if (!liff.isLoggedIn() && !liff.isInClient()) {
        liff.login();
    }

    const access_token = liff.getAccessToken();

    if (access_token !== null) {
        fetch('/golf/' + golf_club['slug'] + '/line-user.json?access_token=' + access_token)
            .then(function (response) {
                return response.json();
            })
            .then(function (result) {
                if (JSON.stringify(result) !== JSON.stringify({})) {
                    fullname.value = result['fullname'];
                    email.value = result['email'];
                    phone.value = result['phone'];
                    lang.value = result['lang'];
                } else {
                    if (!errorModal.classList.contains('is-active')) {
                        errorModal.classList.add('is-active');
                    }
                    errorModalTitle.innerText = 'Failed to get your LINE profile';
                    errorModalBody.innerHTML = 'Please, agree to the terms and conditions and privacy policy.';
                }
            });
    } else {
        if (!errorModal.classList.contains('is-active')) {
            errorModal.classList.add('is-active');
        }
        errorModalTitle.innerText = 'Failed to get your LINE profile';
        errorModalBody.innerHTML = 'Please, agree to the terms and conditions and privacy policy.';
    }
     */

    fullname.value = 'john doe';
    email.value = 'test@example';
    phone.value = '+66801231234';
    lang.value = 'ko';

    // 3. Add event handlers
    document
        .getElementById('save-button')
        .addEventListener('click', function (e) {

            if (validateForm(fullname, email, phone, lang, errorNotification)) {
                if (!bookingConfirmModal.classList.contains('is-active')) {
                    bookingConfirmModal.classList.add('is-active');
                }
                modalTitle.innerText = 'Profile Settings'

                modalBody.innerHTML = `
                    <ul>
                        <li><strong>Customer name</strong>: ${fullname.value}</li>
                        <li><strong>Email</strong>: ${email.value}</li>
                        <li><strong>Telephone</strong>: ${phone.value}</li>
                        <li><strong>Language</strong>: ${lang.value}</li>
                    </ul>
                `;
            }
        });

    [document.getElementById('modal-close'),
        document.getElementById('modal-cancel')].forEach(function (element) {
        element.addEventListener('click', function (e) {
            if (bookingConfirmModal.classList.contains('is-active')) {
                bookingConfirmModal.classList.remove('is-active');
            }
        });
    });

    document
        .getElementById('modal-save')
        .addEventListener('click', function (e) {
            if (validateForm(fullname, email, phone, lang, errorNotification)) {
                if (!liff.isInClient()) {
                    sendAlertIfNotInClient();
                } else {
                    liff.sendMessages([{
                        'type': 'text',
                        'text': 'Settings\n"'
                            + fullname.value + '"\n'
                            + email.value + '\n'
                            + phone.value + '\n'
                            + lang.value
                    }]).then(function () {
                        liff.closeWindow();
                    }).catch(function (error) {
                        if (!errorModal.classList.contains('is-active')) {
                            errorModal.classList.add('is-active');
                        }
                        errorModalTitle.innerText = 'Failed to send message to LINE';
                        errorModalBody.innerHTML = error;
                    });
                }
            }
        });
}