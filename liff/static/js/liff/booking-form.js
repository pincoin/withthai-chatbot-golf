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

document
    .addEventListener('DOMContentLoaded', (event) => {
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

        console.log(today);
        console.log(hour);
        console.log(day);
        console.log(golf_club);
        console.log(fees);
        console.log(holidays);

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
                    pax.value = Number(pax.value) + 1;

                    if ((golf_club['cart_compulsory'] === 0 && Number(cart.value) > 0)
                        || golf_club['cart_compulsory'] === 1
                        || (golf_club['cart_compulsory'] > 1 && Number(pax.value) >= golf_club['cart_compulsory'])
                        || Number(cart.value) >= Number(pax.value)) {
                        cart.value = pax.value;
                    }

                    pax.dispatchEvent(new Event('change'));
                }
            });

        document
            .getElementById('pax-minus-button')
            .addEventListener('click', function (e) {
                if (round_date.value && round_time.value && pax.value > golf_club['min_pax']) {
                    pax.value = Number(pax.value) - 1;

                    if ((golf_club['cart_compulsory'] === 0 && Number(cart.value) > 0)
                        || golf_club['cart_compulsory'] === 1
                        || (golf_club['cart_compulsory'] > 1 && Number(pax.value) >= golf_club['cart_compulsory'])
                        || Number(cart.value) >= Number(pax.value)) {
                        cart.value = pax.value;
                    }

                    pax.dispatchEvent(new Event('change'));
                }
            });

        document
            .getElementById('cart-plus-button')
            .addEventListener('click', function (e) {
                if (round_date.value && round_time.value && cart.value < pax.value) {
                    if (golf_club['cart_compulsory'] === 0
                        || (golf_club['cart_compulsory'] > 1 && Number(pax.value) < golf_club['cart_compulsory'])) {
                        cart.value = Number(cart.value) + 1;
                    }

                    cart.dispatchEvent(new Event('change'));
                }
            });

        document
            .getElementById('cart-minus-button')
            .addEventListener('click', function (e) {
                if (round_date.value && round_time.value && cart.value > 0) {
                    if (golf_club['cart_compulsory'] === 0
                        || (golf_club['cart_compulsory'] > 1 && Number(pax.value) < golf_club['cart_compulsory'])) {
                        cart.value = Number(cart.value) - 1;
                    }

                    cart.dispatchEvent(new Event('change'));
                }
            });

        [round_date, round_time, pax, cart].forEach(function (element) {
            element.addEventListener('change', function (e) {
                if (round_date.value && round_time.value && pax.value && cart.value) {
                    // Calculate green fee
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
    });