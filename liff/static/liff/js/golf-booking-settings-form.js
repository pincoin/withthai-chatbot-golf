const errorModal = document.getElementById('error-modal');
const errorModalTitle = document.getElementById('error-modal-title');
const errorModalBody = document.getElementById('error-modal-body');

let validateFullname = function (fullname, errorNotification) {
    if (fullname.value.trim().match('^[\u0E00-\u0E7F A-Za-z0-9]+$')) {
        return true;
    } else {
        errorNotification.textContent = gettext('Please, type your name in English or Thai.');
        errorNotification.show();
        return false;
    }
}

let validateEmail = function (email, errorNotification) {
    if (email.value.trim().match('[\\w.-]+@[\\w.-]+')) {
        return true;
    } else {
        errorNotification.textContent = gettext('Please, type your valid email address.');
        errorNotification.show();
    }
}

let validatePhone = function (phone, errorNotification) {
    if (phone.value.trim().match('[ \\d+-]{8,18}')) {
        return true;
    } else {
        errorNotification.textContent = gettext('Please, type your valid phone number.');
        errorNotification.show();
    }
}

let validateLang = function (lang, errorNotification) {
    switch (lang.value.trim()) {
        case 'en':
        case 'th':
        case 'ko':
        case 'cn':
        case 'jp':
            return true;
        default:
            errorNotification.textContent = gettext('Please, choose your language.');
            errorNotification.show();
            return false;
    }
}

let validateForm = function (fullname, email, phone, lang, errorNotification) {
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

let runApp = function () {
    // 1. Declares variables
    const fullname = document.getElementById('id_fullname');
    const email = document.getElementById('id_email');
    const phone = document.getElementById('id_phone');
    const lang = document.getElementById('id_lang');

    const bookingConfirmModal = document.getElementById('booking-confirm-modal');
    const modalBody = document.getElementById('modal-body');

    const errorNotification = document.getElementById('error-notification');

    // 2. Retrieve customer group from server using access token
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
                    errorModalTitle.innerText = gettext('Failed to get your LINE profile');
                    errorModalBody.innerHTML = gettext('Please, agree to the terms and conditions and privacy policy.');
                }
            });
    } else {
        if (!errorModal.classList.contains('is-active')) {
            errorModal.classList.add('is-active');
        }
        errorModalTitle.innerText = gettext('Failed to get your LINE profile');
        errorModalBody.innerHTML = gettext('Please, agree to the terms and conditions and privacy policy.');
    }

    // 3. Add event handlers
    document
        .getElementById('save-button')
        .addEventListener('click', function (e) {
            if (validateForm(fullname, email, phone, lang, errorNotification)) {
                if (!bookingConfirmModal.classList.contains('is-active')) {
                    bookingConfirmModal.classList.add('is-active');
                }
                modalBody.innerHTML =
                    "<ul>" +
                    "<li><strong>" + gettext('Customer name') + "</strong>: " + fullname.value + "</li>" +
                    "<li><strong>" + gettext('Email') + "</strong>: " + email.value + "</li>" +
                    "<li><strong>" + gettext('Telephone') + "</strong>: " + phone.value + "</li>" +
                    "<li><strong>" + gettext('Language') + "</strong>: " + lang.value + "</li>" +
                    "</ul>";
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
                        'text': "Settings\n" +
                            '"' + fullname.value.trim() + '"\n'
                            + email.value.trim() + '\n'
                            + phone.value.trim() + '\n'
                            + lang.value.trim()
                    }]).then(function () {
                        liff.closeWindow();
                    }).catch(function (error) {
                        if (!errorModal.classList.contains('is-active')) {
                            errorModal.classList.add('is-active');
                        }
                        errorModalTitle.innerText = gettext('Failed to send message to LINE');
                        errorModalBody.innerHTML = error;
                    });
                }
            }
        });
}