Date.prototype.formatDate = function () {
    return this.getFullYear()
        + '-' + ('0' + (this.getMonth() + 1)).slice(-2)
        + '-' + ('0' + this.getDate()).slice(-2);
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

function calculateFees(roundDate, roundTime, pax, cart, customerGroup, today, hour, day) {
    const roundDateElements = roundDate.value.split('-');
    const roundTimeElements = roundTime.value.split(':');

    const roundDateObject = new Date(Number(roundDateElements[0]),
        Number(roundDateElements[1]) - 1,
        Number(roundDateElements[2]));

    const roundTimeObject = new Date(2020, 0, 1,
        Number(roundTimeElements[0]),
        Number(roundTimeElements[1]));

    let weekday = isHoliday(roundDateObject);

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
}

function displayQuotation(greenFeeUnitPrice, greenFeePax, greenFeeAmount,
                          caddieFeeUnitPrice, caddieFeePax, caddieFeeAmount,
                          cartFeeUnitPrice, cartFeePax, cartFeeAmount, feeTotalAmount, fee, pax, cart) {
    greenFeeUnitPrice.textContent = fee['greenFee'].toLocaleString('en');
    greenFeePax.textContent = Number(pax.value);
    greenFeeAmount.textContent = (fee['greenFee'] * Number(pax.value)).toLocaleString('en');

    caddieFeeUnitPrice.textContent = fee['caddieFee'].toLocaleString('en');
    caddieFeePax.textContent = Number(pax.value);
    caddieFeeAmount.textContent = (fee['caddieFee'] * Number(pax.value)).toLocaleString('en');

    cartFeeUnitPrice.textContent = fee['cartFee'].toLocaleString('en');
    cartFeePax.textContent = Number(cart.value);
    cartFeeAmount.textContent = (fee['cartFee'] * Number(cart.value)).toLocaleString('en');

    feeTotalAmount.textContent = ((fee['greenFee'] + fee['caddieFee']) * Number(pax.value)
        + fee['cartFee'] * Number(cart.value)).toLocaleString('en');
}

function validateRoundDate(roundDate) {
    console.log(roundDate.value);

    /*
    if (weekday === 0
        || (weekday === 1
            && round_date_object.getTime() - today.getTime() < golf_club['weekend_max_in_advance'] * 24 * 60 * 60 * 1000)
        && day.toUpperCase() !== 'SAT'
        && day.toUpperCase() !== 'SUN') {
    }
    */
}

function validateRoundTime(roundTime) {
    console.log(roundTime.value);
}

function validateForm(roundDate, roundTime, pax, cart, customerGroup) {
    validateRoundDate(roundDate);

    validateRoundTime(roundTime);

    console.log(pax.value);
    console.log(cart.value);
    console.log(customerGroup.value);
}

function runApp() {
    let roundDate = document.getElementById('id_round_date');
    let roundTime = document.getElementById('id_round_time');
    let pax = document.getElementById('id_pax');
    let cart = document.getElementById('id_cart');
    let customerName = document.getElementById('id_customer_name');

    let greenFeeUnitPrice = document.getElementById('green-fee-unit-price');
    let greenFeePax = document.getElementById('green-fee-pax');
    let greenFeeAmount = document.getElementById('green-fee-amount');

    let caddieFeeUnitPrice = document.getElementById('caddie-fee-unit-price');
    let caddieFeePax = document.getElementById('caddie-fee-pax');
    let caddieFeeAmount = document.getElementById('caddie-fee-amount');

    let cartFeeUnitPrice = document.getElementById('cart-fee-unit-price');
    let cartFeePax = document.getElementById('cart-fee-pax');
    let cartFeeAmount = document.getElementById('cart-fee-amount');

    let feeTotalAmount = document.getElementById('fee-total-amount');

    let customerGroup = 0;

    const today = new Date();
    const hour = today.toLocaleString('en-US', {
        timeZone: 'Asia/Bangkok',
        hour: 'numeric',
        hour12: false
    });
    const day = today.toLocaleString('en-US', {
        timeZone: 'Asia/Bangkok',
        weekday: 'short',
    });

    // 1. Arrange round date and time range
    let minDate = new Date(today);
    let maxDate = new Date(today);

    if (hour >= golf_club['business_hour_end'].split(':')[0] && hour < 24) {
        minDate.setDate(minDate.getDate() + golf_club['weekdays_min_in_advance'] + 1);
        maxDate.setDate(maxDate.getDate() + golf_club['weekdays_max_in_advance'] + 1);
    } else {
        minDate.setDate(minDate.getDate() + golf_club['weekdays_min_in_advance']);
        maxDate.setDate(maxDate.getDate() + golf_club['weekdays_max_in_advance']);
    }

    roundDate.value = minDate.formatDate();
    roundDate.setAttribute('min', minDate.formatDate());
    roundDate.setAttribute('max', maxDate.formatDate());

    let roundTimeStart = fees[0]['slot_start'];
    let roundTimeEnd = fees[fees.length - 1]['slot_end'];

    roundTime.value = roundTimeStart;
    roundTime.setAttribute('min', roundTimeStart);
    roundTime.setAttribute('max', roundTimeEnd);

    if (liff.isLoggedIn() && liff.isInClient()) {
        liff.getProfile().then(function (profile) {
            fetch('/golf/' + golf_club['slug'] + '/' + profile.userId + '/customer-group.json')
                .then(function (response) {
                    return response.json();
                })
                .then(function (myJson) {
                    customerGroup = myJson['customer_group_id'];

                    if (roundDate.value && roundTime.value && pax.value && cart.value) {
                        const fee = calculateFees(roundDate, roundTime, pax, cart, customerGroup, today, hour, day);

                        displayQuotation(greenFeeUnitPrice, greenFeePax, greenFeeAmount,
                            caddieFeeUnitPrice, caddieFeePax, caddieFeeAmount,
                            cartFeeUnitPrice, cartFeePax, cartFeeAmount, feeTotalAmount, fee, pax, cart);
                    }
                });
        }).catch(function (error) {
            window.alert('Error getting profile: ' + error);
        });
    } else {
        customerGroup = 4;

        if (roundDate.value && roundTime.value && pax.value && cart.value) {
            const fee = calculateFees(roundDate, roundTime, pax, cart, customerGroup, today, hour, day);

            displayQuotation(greenFeeUnitPrice, greenFeePax, greenFeeAmount,
                caddieFeeUnitPrice, caddieFeePax, caddieFeeAmount,
                cartFeeUnitPrice, cartFeePax, cartFeeAmount, feeTotalAmount, fee, pax, cart);
        }
    }

    // 2. Event handlers
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
                const fee = calculateFees(roundDate, roundTime, pax, cart, customerGroup, today, hour, day);

                displayQuotation(greenFeeUnitPrice, greenFeePax, greenFeeAmount,
                    caddieFeeUnitPrice, caddieFeePax, caddieFeeAmount,
                    cartFeeUnitPrice, cartFeePax, cartFeeAmount, feeTotalAmount, fee, pax, cart);
            }
        });
    });

    document
        .getElementById('new-booking-button')
        .addEventListener('click', function (e) {
            validateForm(roundDate, roundTime, pax, cart, customerName);
        });
}
