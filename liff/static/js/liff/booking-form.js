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

    if (liff.isLoggedIn() && liff.isInClient()) {
        liff.getProfile().then(function (profile) {
            fetch('/golf/' + golf_club['slug'] + '/' + profile.userId + '/customer-group.json')
                .then(function (response) {
                    return response.json();
                })
                .then(function (myJson) {
                    window.alert(JSON.stringify(myJson)['customer_group_id']);
                });
        }).catch(function (error) {
            window.alert('Error getting profile: ' + error);
        });
    } else {
        customer_group = 4;
    }

    console.log(today);
    console.log(hour);
    console.log(day);
    console.log(golf_club);
    console.log(fees);
    console.log(holidays);
    console.log(customer_group);

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
                const round_date_elements = round_date.value.split('-');
                const round_time_elements = round_time.value.split(':');

                const rdate = new Date(Number(round_date_elements[0]),
                    Number(round_date_elements[1]) - 1,
                    Number(round_date_elements[2]));

                const rtime = new Date(2020, 0, 1,
                    Number(round_time_elements[0]),
                    Number(round_time_elements[1]));

                // Check if round date is  weekend
                let weekday = 0;

                if (rdate.getDay() === 6 || rdate.getDay() === 0) {
                    weekday = 1;
                }

                // Check if round date is public holiday
                let out = false;

                for (i = 0; i < holidays.length; i++) {
                    const holiday = holidays[i].split('-');

                    if (rdate.getTime() === new Date(Number(holiday[0]),
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

                let out1 = false;

                // 4. Calculate fees
                if (weekday === 0
                    || (weekday === 1
                        && rdate.getTime() - today.getTime() < golf_club['weekend_max_in_advance'] * 24 * 60 * 60 * 1000)
                    && day.toUpperCase() !== 'SAT'
                    && day.toUpperCase() !== 'SUN') {
                    for (i = 0; i < fees.length; i++) {
                        if (fees[i]['weekday'] === weekday) {
                            // check whether round date is within season
                            const season_start = fees[i]['season_start'].split('-');
                            const season_end = fees[i]['season_end'].split('-');

                            if (rdate.getTime() >= new Date(Number(season_start[0]),
                                Number(season_start[1]) - 1,
                                Number(season_start[2])).getTime()
                                && rdate.getTime() <= new Date(Number(season_end[0]),
                                    Number(season_end[1]) - 1,
                                    Number(season_end[2])).getTime()) {
                                // check whether round time is within available slot time
                                const slot_start = fees[i]['slot_start'].split(':');
                                const slot_end = fees[i]['slot_end'].split(':');

                                if (rtime.getTime() >= new Date(2020, 0, 1,
                                    Number(slot_start[0]), Number(slot_start[1]))
                                    && rtime.getTime() <= new Date(2020, 0, 1,
                                        Number(slot_end[0]), Number(slot_end[1]))) {

                                    out1 = true;
                                    break;
                                }
                            }
                        }
                        if (out1) {
                            break;
                        }
                    }
                }
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
