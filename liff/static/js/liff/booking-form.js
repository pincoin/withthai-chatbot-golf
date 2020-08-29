Date.prototype.formatDate = function () {
    return this.getFullYear()
        + '-' + ('0' + (this.getMonth() + 1)).slice(-2)
        + '-' + ('0' + this.getDate()).slice(-2);
}

HTMLElement.prototype.show = function () {
    if (this.classList.contains('is-hidden')) {
        this.classList.remove('is-hidden');
    }
}

HTMLElement.prototype.hide = function () {
    if (!this.classList.contains('is-hidden')) {
        this.textContent = '';
        this.classList.add('is-hidden');
    }
}

HTMLElement.prototype.toggle = function () {
    if (this.classList.contains('is-hidden')) {
        this.classList.remove('is-hidden');
    } else {
        this.textContent = '';
        this.classList.add('is-hidden');
    }
}

HTMLElement.prototype.error_field = function () {
    if (!this.classList.contains('is-danger')) {
        this.classList.add('is-danger');
    }
}

HTMLElement.prototype.clear_error_field = function () {
    if (this.classList.contains('is-danger')) {
        this.classList.remove('is-danger');
    }
}

function getCurrentTime() {
    const now = new Date();

    return {
        'date': now,
        'hour': now.toLocaleString('en-US', {
            timeZone: 'Asia/Bangkok',
            hour: 'numeric',
            hour12: false
        }),
        'day': now.toLocaleString('en-US', {
            timeZone: 'Asia/Bangkok',
            weekday: 'short',
        }).toUpperCase()
    }
}

function isHoliday(roundDate) {
    // return 0: Weekday 1: Holiday

    // Weekend Saturday and Sunday
    if (roundDate.getDay() === 6 || roundDate.getDay() === 0) {
        return 1;
    }
    // Public holidays
    for (let i = 0; i < holidays.length; i++) {
        const holiday = holidays[i].split('-');

        if (roundDate.getTime() === new Date(Number(holiday[0]),
            Number(holiday[1]) - 1,
            Number(holiday[2])).getTime()) {
            return 1;
        }
    }
    return 0;
}

function setCartByPax(cart, pax, cartCompulsory, diff) {
    pax.value = Number(pax.value) + diff;

    if ((cartCompulsory === 0 && Number(cart.value) > 0)
        || cartCompulsory === 1
        || (cartCompulsory > 1 && Number(pax.value) >= cartCompulsory)
        || Number(cart.value) >= Number(pax.value)) {
        cart.value = pax.value;
    }
}

function setCart(cart, pax, cartCompulsory, diff) {
    if (cartCompulsory === 0
        || (cartCompulsory > 1 && Number(pax.value) < cartCompulsory)) {
        cart.value = Number(cart.value) + diff;
    }
}

function calculateFees(roundDate, roundTime, pax, cart, customerGroup) {
    const roundDateElements = roundDate.value.split('-');
    const roundTimeElements = roundTime.value.split(':');

    const roundDateObject = new Date(Number(roundDateElements[0]),
        Number(roundDateElements[1]) - 1,
        Number(roundDateElements[2]));

    const roundTimeObject = new Date(2020, 0, 1,
        Number(roundTimeElements[0]),
        Number(roundTimeElements[1]));

    const weekday = isHoliday(roundDateObject);

    for (let i = 0; i < fees.length; i++) {
        if (customerGroup !== fees[i]['customer_group']) {
            continue;
        }
        if (fees[i]['weekday'] !== weekday) {
            continue;
        }
        const sessionStart = fees[i]['season_start'].split('-');
        const sessionEnd = fees[i]['season_end'].split('-');

        if (roundDateObject.getTime() < new Date(Number(sessionStart[0]),
            Number(sessionStart[1]) - 1,
            Number(sessionStart[2])).getTime()
            || roundDateObject.getTime() > new Date(Number(sessionEnd[0]),
                Number(sessionEnd[1]) - 1,
                Number(sessionEnd[2])).getTime()) {
            continue;
        }

        const timeslotStart = fees[i]['slot_start'].split(':');
        const timeslotEnd = fees[i]['slot_end'].split(':');

        if (roundTimeObject.getTime() < new Date(2020, 0, 1,
            Number(timeslotStart[0]), Number(timeslotStart[1]))
            || roundTimeObject.getTime() > new Date(2020, 0, 1,
                Number(timeslotEnd[0]), Number(timeslotEnd[1]))) {
            continue;
        }

        return {
            'greenFee': fees[i]['green_fee'],
            'caddieFee': fees[i]['caddie_fee'],
            'cartFee': fees[i]['cart_fee']
        }
    }

    window.alert('Invalid round date or time');
    return false;
}

function displayQuotation(greenFeeUnitPrice, greenFeePax, greenFeeAmount,
                          caddieFeeUnitPrice, caddieFeePax, caddieFeeAmount,
                          cartFeeUnitPrice, cartFeePax, cartFeeAmount,
                          feeTotalAmount, fee, pax, cart) {
    greenFeePax.textContent = Number(pax.value);
    caddieFeePax.textContent = Number(pax.value);
    cartFeePax.textContent = Number(cart.value);

    if (fee !== false) {
        greenFeeUnitPrice.textContent = fee['greenFee'].toLocaleString('en');
        greenFeeAmount.textContent = (fee['greenFee'] * Number(pax.value)).toLocaleString('en');

        caddieFeeUnitPrice.textContent = fee['caddieFee'].toLocaleString('en');
        caddieFeeAmount.textContent = (fee['caddieFee'] * Number(pax.value)).toLocaleString('en');

        cartFeeUnitPrice.textContent = fee['cartFee'].toLocaleString('en');
        cartFeeAmount.textContent = (fee['cartFee'] * Number(cart.value)).toLocaleString('en');

        feeTotalAmount.textContent = ((fee['greenFee'] + fee['caddieFee']) * Number(pax.value)
            + fee['cartFee'] * Number(cart.value)).toLocaleString('en');
    } else {
        [greenFeeUnitPrice, greenFeeAmount,
            caddieFeeUnitPrice, caddieFeeAmount,
            cartFeeUnitPrice, cartFeeAmount,
            feeTotalAmount].forEach(function (element) {
            element.textContent = 'N/A';
        });
    }
}

function validateRoundDate(roundDate, errorNotification) {
    const roundDateElements = roundDate.value.split('-');

    const roundDateObject = new Date(Number(roundDateElements[0]),
        Number(roundDateElements[1]) - 1,
        Number(roundDateElements[2]));

    const weekday = isHoliday(roundDateObject);

    const now = getCurrentTime();

    if (weekday === 0
        && roundDateObject.getTime() - now['date'].getTime()
        > golf_club['weekday_max_in_advance'] * 24 * 60 * 60 * 1000) {
        roundDate.error_field();

        errorNotification.textContent = 'Round date is not available.';
        errorNotification.show();
        return false;
    } else if (weekday === 1) {
        if (roundDateObject.getTime() - now['date'].getTime()
            > golf_club['weekend_max_in_advance'] * 24 * 60 * 60 * 1000
            || now['day'] === 'SAT' || now['day'] === 'SUN') {
            roundDate.error_field();

            errorNotification.textContent = 'Round date is not available.';
            errorNotification.show();
            return false;
        }
    }
    return true;
}

function validateRoundTime(roundTime, errorNotification) {
    const roundTimeElements = roundTime.value.split(':');

    const roundTimeStartElements = fees[0]['slot_start'].split(':');
    const roundTimeEndElements = fees[fees.length - 1]['slot_end'].split(':');

    const roundTimeObject = new Date(2020, 0, 1,
        Number(roundTimeElements[0]),
        Number(roundTimeElements[1]));

    if (roundTimeObject.getTime() < new Date(2020, 0, 1,
        Number(roundTimeStartElements[0]), Number(roundTimeStartElements[1]))
        || roundTimeObject.getTime() > new Date(2020, 0, 1,
            Number(roundTimeEndElements[0]), Number(roundTimeEndElements[1]))) {
        roundTime.error_field();

        errorNotification.textContent = 'Round time is not available.';
        errorNotification.show();
        return false;
    }
    return true;
}

function validatePax(pax, errorNotification) {
    if (Number(pax.value) < golf_club['min_pax'] || Number(pax.value) > golf_club['max_pax']) {
        pax.error_field();

        errorNotification.textContent = 'PAX is not available.';
        errorNotification.show();
        return false;
    }
    return true;
}

function validateCart(cart, errorNotification) {
    let min_pax = 0;

    if (golf_club['cart_compulsory'] === 0) {
        min_pax = 0;
    } else if (golf_club['cart_compulsory'] === 1) {
        min_pax = golf_club['min_pax'];
    } else if (golf_club['cart_compulsory'] > 1) {
        if (golf_club['cart_compulsory'] > 1 && golf_club['cart_compulsory'] > golf_club['min_pax'] > 1) {
            min_pax = golf_club['min_pax'];
        } else {
            min_pax = 0;
        }
    }
    if (Number(cart.value) > golf_club['max_pax'] || Number(cart.value) < min_pax) {
        cart.error_field();

        errorNotification.textContent = 'Cart is not available.';
        errorNotification.show();
        return false;
    }
    return true;
}

function validateCustomerName(customerName, errorNotification) {
    if (!customerName.value || 0 === customerName.length) {
        customerName.error_field();

        errorNotification.textContent = 'Please, type your name in Thai or English.';
        errorNotification.show();
        return false;
    }
    if (customerName.value.match(/^[\u0E00-\u0E7F a-zA-Z0-9.,]+$/g) === null) {
        customerName.error_field();

        errorNotification.textContent = 'Your name must be written in Thai or English.';
        errorNotification.show();
        return false;
    }
    return true;
}

function validateForm(roundDate, roundTime, pax, cart, customerName, errorNotification) {
    if (!validateRoundDate(roundDate, errorNotification)) {
        return false;
    }
    if (!validateRoundTime(roundTime, errorNotification)) {
        return false;
    }
    if (!validatePax(pax, errorNotification)) {
        return false;
    }
    if (!validateCart(cart, errorNotification)) {
        return false;
    }
    return validateCustomerName(customerName, errorNotification);
}

function runApp() {
    const roundDate = document.getElementById('id_round_date');
    const roundTime = document.getElementById('id_round_time');
    const pax = document.getElementById('id_pax');
    const cart = document.getElementById('id_cart');
    const customerName = document.getElementById('id_customer_name');

    const greenFeeUnitPrice = document.getElementById('green-fee-unit-price');
    const greenFeePax = document.getElementById('green-fee-pax');
    const greenFeeAmount = document.getElementById('green-fee-amount');

    const caddieFeeUnitPrice = document.getElementById('caddie-fee-unit-price');
    const caddieFeePax = document.getElementById('caddie-fee-pax');
    const caddieFeeAmount = document.getElementById('caddie-fee-amount');

    const cartFeeUnitPrice = document.getElementById('cart-fee-unit-price');
    const cartFeePax = document.getElementById('cart-fee-pax');
    const cartFeeAmount = document.getElementById('cart-fee-amount');

    const feeTotalAmount = document.getElementById('fee-total-amount');

    const errorNotification = document.getElementById('error-notification');

    let customerGroup = 0;

    const now = getCurrentTime();

    // 1. Initialize round date and time range form
    const minDate = new Date(now['date']);
    const maxDate = new Date(now['date']);

    if (now['hour'] >= golf_club['business_hour_end'].split(':')[0] && now['hour'] < 24) {
        minDate.setDate(minDate.getDate() + golf_club['weekdays_min_in_advance'] + 1);
        maxDate.setDate(maxDate.getDate() + golf_club['weekdays_max_in_advance'] + 1);
    } else {
        minDate.setDate(minDate.getDate() + golf_club['weekdays_min_in_advance']);
        maxDate.setDate(maxDate.getDate() + golf_club['weekdays_max_in_advance']);
    }

    roundDate.value = minDate.formatDate();
    roundDate.setAttribute('min', minDate.formatDate());
    roundDate.setAttribute('max', maxDate.formatDate());

    const roundTimeStart = fees[0]['slot_start'];
    const roundTimeEnd = fees[fees.length - 1]['slot_end'];

    roundTime.value = roundTimeStart;
    roundTime.setAttribute('min', roundTimeStart);
    roundTime.setAttribute('max', roundTimeEnd);

    if (!liff.isLoggedIn() && !liff.isInClient()) {
        liff.login();
    }

    // 2. Retrieve customer group from server using access token
    const access_token = liff.getAccessToken();

    fetch('/golf/' + golf_club['slug'] + '/customer-group.json?access_token=' + access_token)
        .then(function (response) {
            return response.json();
        })
        .then(function (myJson) {
            customerGroup = myJson['customer_group_id'];

            if (roundDate.value && roundTime.value && pax.value && cart.value) {
                const fee = calculateFees(roundDate, roundTime, pax, cart, customerGroup);

                displayQuotation(greenFeeUnitPrice, greenFeePax, greenFeeAmount,
                    caddieFeeUnitPrice, caddieFeePax, caddieFeeAmount,
                    cartFeeUnitPrice, cartFeePax, cartFeeAmount, feeTotalAmount, fee, pax, cart);
            }
        });

    // 3. Add event handlers
    document
        .getElementById('pax-plus-button')
        .addEventListener('click', function (e) {
            if (roundDate.value && roundTime.value && pax.value < golf_club['max_pax']) {
                setCartByPax(cart, pax, golf_club['cart_compulsory'], 1);
                pax.dispatchEvent(new Event('change'));
            }
        });

    document
        .getElementById('pax-minus-button')
        .addEventListener('click', function (e) {
            if (roundDate.value && roundTime.value && pax.value > golf_club['min_pax']) {
                setCartByPax(cart, pax, golf_club['cart_compulsory'], -1);
                pax.dispatchEvent(new Event('change'));
            }
        });

    document
        .getElementById('cart-plus-button')
        .addEventListener('click', function (e) {
            if (roundDate.value && roundTime.value && cart.value < pax.value) {
                setCart(cart, pax, golf_club['cart_compulsory'], 1);
                cart.dispatchEvent(new Event('change'));
            }
        });

    document
        .getElementById('cart-minus-button')
        .addEventListener('click', function (e) {
            if (roundDate.value && roundTime.value && cart.value > 0) {
                setCart(cart, pax, golf_club['cart_compulsory'], -1);
                cart.dispatchEvent(new Event('change'));
            }
        });

    [roundDate, roundTime, pax, cart].forEach(function (element) {
        element.addEventListener('change', function (e) {
            if (roundDate.value && roundTime.value && pax.value && cart.value) {
                errorNotification.hide();

                [roundDate, roundTime, pax, cart].forEach(function (element) {
                    element.clear_error_field();
                });

                if (validateRoundDate(roundDate, errorNotification)
                    && validateRoundTime(roundTime, errorNotification)
                    && validatePax(pax, errorNotification)
                    && validateCart(cart, errorNotification)) {
                    const fee = calculateFees(roundDate, roundTime, pax, cart, customerGroup);

                    displayQuotation(greenFeeUnitPrice, greenFeePax, greenFeeAmount,
                        caddieFeeUnitPrice, caddieFeePax, caddieFeeAmount,
                        cartFeeUnitPrice, cartFeePax, cartFeeAmount, feeTotalAmount, fee, pax, cart);
                } else {
                    displayQuotation(greenFeeUnitPrice, greenFeePax, greenFeeAmount,
                        caddieFeeUnitPrice, caddieFeePax, caddieFeeAmount,
                        cartFeeUnitPrice, cartFeePax, cartFeeAmount, feeTotalAmount, false, pax, cart);
                }
            }
        });
    });

    document
        .getElementById('new-booking-button')
        .addEventListener('click', function (e) {
            validateForm(roundDate, roundTime, pax, cart, customerName, errorNotification);
        });
}
