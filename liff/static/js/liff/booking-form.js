function formatDate(date) {
    let month = '' + (date.getMonth() + 1);
    let day = '' + date.getDate();
    let year = date.getFullYear();

    if (month.length < 2)
        month = '0' + month;
    if (day.length < 2)
        day = '0' + day;

    return [year, month, day].join('-');
}

function iskHoliday(round_date) {
    // Weekend Saturday and Sunday
    let weekday = 0;

    if (round_date.getDay() === 6 || round_date.getDay() === 0) {
        weekday = 1;
    }

    // Public holidays
    let out = false;

    for (i = 0; i < holidays.length; i++) {
        const holiday = holidays[i].split('-');

        if (round_date.getTime() === new Date(Number(holiday[0]),
            Number(holiday[1]) - 1,
            Number(holiday[2])).getTime()) {
            out = true;
            weekday = 1;
            break;
        }

        if (out) {
            break;
        }
    }

    // 0: Weekday 1: Holiday
    return weekday;
}

function setCartByPax(cart, pax, cart_compulsory, diff) {
    pax.value = Number(pax.value) + diff;

    if ((cart_compulsory === 0 && Number(cart.value) > 0)
        || cart_compulsory === 1
        || (cart_compulsory > 1 && Number(pax.value) >= cart_compulsory)
        || Number(cart.value) >= Number(pax.value)) {
        cart.value = pax.value;
    }
}

function setCart(cart, pax, cart_compulsory, diff) {
    if (cart_compulsory === 0
        || (cart_compulsory > 1 && Number(pax.value) < cart_compulsory)) {
        cart.value = Number(cart.value) + diff;
    }
}

function calculateFees(round_date, round_time, pax, cart, customer_group, today, hour, day) {
    const round_date_elements = round_date.value.split('-');
    const round_time_elements = round_time.value.split(':');

    const round_date_object = new Date(Number(round_date_elements[0]),
        Number(round_date_elements[1]) - 1,
        Number(round_date_elements[2]));

    const round_time_object = new Date(2020, 0, 1,
        Number(round_time_elements[0]),
        Number(round_time_elements[1]));

    let weekday = iskHoliday(round_date_object);

    for (let i = 0; i < fees.length; i++) {
        if (customer_group !== fees[i]['customer_group']) {
            continue;
        }
        if (fees[i]['weekday'] !== weekday) {
            continue;
        }
        const season_start = fees[i]['season_start'].split('-');
        const season_end = fees[i]['season_end'].split('-');

        if (round_date_object.getTime() < new Date(Number(season_start[0]),
            Number(season_start[1]) - 1,
            Number(season_start[2])).getTime()
            || round_date_object.getTime() > new Date(Number(season_end[0]),
                Number(season_end[1]) - 1,
                Number(season_end[2])).getTime()) {
            continue;
        }

        const slot_start = fees[i]['slot_start'].split(':');
        const slot_end = fees[i]['slot_end'].split(':');

        if (round_time_object.getTime() < new Date(2020, 0, 1,
            Number(slot_start[0]), Number(slot_start[1]))
            || round_time_object.getTime() > new Date(2020, 0, 1,
                Number(slot_end[0]), Number(slot_end[1]))) {
            continue;
        }

        return {
            'green_fee': fees[i]['green_fee'],
            'caddie_fee': fees[i]['caddie_fee'],
            'cart_fee': fees[i]['cart_fee']
        }
    }

    /*
    if (weekday === 0
        || (weekday === 1
            && round_date_object.getTime() - today.getTime() < golf_club['weekend_max_in_advance'] * 24 * 60 * 60 * 1000)
        && day.toUpperCase() !== 'SAT'
        && day.toUpperCase() !== 'SUN') {
    }
    */
}

function display_quotation(green_fee_unit_price, green_fee_pax, green_fee_amount,
                           caddie_fee_unit_price, caddie_fee_pax, caddie_fee_amount,
                           cart_fee_unit_price, cart_fee_pax, cart_fee_amount, fee_total_amount, fee, pax, cart) {
    green_fee_unit_price.textContent = fee['green_fee'];
    green_fee_pax.textContent = Number(pax.value);
    green_fee_amount.textContent = fee['green_fee'] * Number(pax.value);

    caddie_fee_unit_price.textContent = fee['caddie_fee'];
    caddie_fee_pax.textContent = Number(pax.value);
    caddie_fee_amount.textContent = fee['caddie_fee'] * Number(pax.value);

    cart_fee_unit_price.textContent = fee['cart_fee'];
    cart_fee_pax.textContent = Number(cart.value);
    cart_fee_amount.textContent = fee['cart_fee'] * Number(cart.value);

    fee_total_amount.textContent = (fee['green_fee'] + fee['caddie_fee']) * Number(pax.value)
        + fee['cart_fee'] * Number(cart.value);
}

function runApp() {
    let round_date = document.getElementById('id_round_date');
    let round_time = document.getElementById('id_round_time');
    let pax = document.getElementById('id_pax');
    let cart = document.getElementById('id_cart');

    let green_fee_unit_price = document.getElementById('green-fee-unit-price');
    let green_fee_pax = document.getElementById('green-fee-pax');
    let green_fee_amount = document.getElementById('green-fee-amount');

    let caddie_fee_unit_price = document.getElementById('caddie-fee-unit-price');
    let caddie_fee_pax = document.getElementById('caddie-fee-pax');
    let caddie_fee_amount = document.getElementById('caddie-fee-amount');

    let cart_fee_unit_price = document.getElementById('cart-fee-unit-price');
    let cart_fee_pax = document.getElementById('cart-fee-pax');
    let cart_fee_amount = document.getElementById('cart-fee-amount');

    let fee_total_amount = document.getElementById('fee-total-amount');

    let customer_group = 0;

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
    let min_date = new Date(today);
    let max_date = new Date(today);

    if (hour >= golf_club['business_hour_end'].split(':')[0] && hour < 24) {
        min_date.setDate(min_date.getDate() + golf_club['weekdays_min_in_advance'] + 1);
        max_date.setDate(max_date.getDate() + golf_club['weekdays_max_in_advance'] + 1);
    } else {
        min_date.setDate(min_date.getDate() + golf_club['weekdays_min_in_advance']);
        max_date.setDate(max_date.getDate() + golf_club['weekdays_max_in_advance']);
    }

    round_date.value = formatDate(min_date);
    round_date.setAttribute('min', formatDate(min_date));
    round_date.setAttribute('max', formatDate(max_date));

    let round_time_start = fees[0]['slot_start'];
    let round_time_end = fees[fees.length - 1]['slot_end'];

    round_time.value = round_time_start;
    round_time.setAttribute('min', round_time_start);
    round_time.setAttribute('max', round_time_end);

    if (liff.isLoggedIn() && liff.isInClient()) {
        liff.getProfile().then(function (profile) {
            fetch('/golf/' + golf_club['slug'] + '/' + profile.userId + '/customer-group.json')
                .then(function (response) {
                    return response.json();
                })
                .then(function (myJson) {
                    customer_group = myJson['customer_group_id'];

                    if (round_date.value && round_time.value && pax.value && cart.value) {
                        const fee = calculateFees(round_date, round_time, pax, cart, customer_group, today, hour, day);

                        display_quotation(green_fee_unit_price, green_fee_pax, green_fee_amount,
                            caddie_fee_unit_price, caddie_fee_pax, caddie_fee_amount,
                            cart_fee_unit_price, cart_fee_pax, cart_fee_amount, fee_total_amount, fee, pax, cart);
                    }
                });
        }).catch(function (error) {
            window.alert('Error getting profile: ' + error);
        });
    } else {
        customer_group = 4;

        if (round_date.value && round_time.value && pax.value && cart.value) {
            const fee = calculateFees(round_date, round_time, pax, cart, customer_group, today, hour, day);

            display_quotation(green_fee_unit_price, green_fee_pax, green_fee_amount,
                caddie_fee_unit_price, caddie_fee_pax, caddie_fee_amount,
                cart_fee_unit_price, cart_fee_pax, cart_fee_amount, fee_total_amount, fee, pax, cart);
        }
    }

    // 2. Event handlers
    document
        .getElementById('pax-plus-button')
        .addEventListener('click', function (e) {
            if (round_date.value && round_time.value && pax.value < golf_club['max_pax']) {
                setCartByPax(cart, pax, golf_club['cart_compulsory'], 1);
                pax.dispatchEvent(new Event('change'));
            }
        });

    document
        .getElementById('pax-minus-button')
        .addEventListener('click', function (e) {
            if (round_date.value && round_time.value && pax.value > golf_club['min_pax']) {
                setCartByPax(cart, pax, golf_club['cart_compulsory'], -1);
                pax.dispatchEvent(new Event('change'));
            }
        });

    document
        .getElementById('cart-plus-button')
        .addEventListener('click', function (e) {
            if (round_date.value && round_time.value && cart.value < pax.value) {
                setCart(cart, pax, golf_club['cart_compulsory'], 1);
                cart.dispatchEvent(new Event('change'));
            }
        });

    document
        .getElementById('cart-minus-button')
        .addEventListener('click', function (e) {
            if (round_date.value && round_time.value && cart.value > 0) {
                setCart(cart, pax, golf_club['cart_compulsory'], -1);
                cart.dispatchEvent(new Event('change'));
            }
        });

    [round_date, round_time, pax, cart].forEach(function (element) {
        element.addEventListener('change', function (e) {
            if (round_date.value && round_time.value && pax.value && cart.value) {
                const fee = calculateFees(round_date, round_time, pax, cart, customer_group, today, hour, day);

                display_quotation(green_fee_unit_price, green_fee_pax, green_fee_amount,
                    caddie_fee_unit_price, caddie_fee_pax, caddie_fee_amount,
                    cart_fee_unit_price, cart_fee_pax, cart_fee_amount, fee_total_amount, fee, pax, cart);
            }
        });
    });

    document
        .getElementById('new-booking-button')
        .addEventListener('click', function (e) {
            // Form validation
            // 1-1. round_date
            console.log(round_date.value);

            // 1-2. round_time
            console.log(round_time.value);

            // 1-4. pax
            console.log(pax.value);

            // 1-4. cart
            console.log(cart.value);
        });
}
