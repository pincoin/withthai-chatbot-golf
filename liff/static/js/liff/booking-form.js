function formatDate(date) {
    month = '' + (date.getMonth() + 1);
    day = '' + date.getDate();
    year = date.getFullYear();

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

        if (hour >= 17 && hour < 24) {
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
        let round_time_end = fees[0]['slot_end'];

        for (i = 1; i < fees.length; i++) {
            if (round_time_start > fees[i]['slot_start']) {
                round_time_start = fees[i]['slot_start'];
            }

            if (round_time_end < fees[i]['slot_end']) {
                round_time_end = fees[i]['slot_end'];
            }
        }

        round_time.value = round_time_start;
        round_time.setAttribute('min', round_time_start);
        round_time.setAttribute('max', round_time_end);

        document
            .getElementById('pax-plus-button')
            .addEventListener('click', function (e) {
                pax.value = Number(pax.value) + 1;
                pax.dispatchEvent(new Event('change'));
            });

        document
            .getElementById('pax-minus-button')
            .addEventListener('click', function (e) {
                pax.value = Number(pax.value) - 1;
                pax.dispatchEvent(new Event('change'));
            });

        document
            .getElementById('cart-plus-button')
            .addEventListener('click', function (e) {
                cart.value = Number(cart.value) + 1;
                cart.dispatchEvent(new Event('change'));
            });

        document
            .getElementById('cart-minus-button')
            .addEventListener('click', function (e) {
                cart.value = Number(cart.value) - 1;
                cart.dispatchEvent(new Event('change'));
            });

        [round_date, round_time, pax, cart].forEach(function (element) {
            element.addEventListener('change', function (e) {
                if (round_date.value && round_time.value && pax.value && cart.value) {
                    // 1. 검증
                    // 1-1. round_date 예약 가능 일자
                    console.log(round_date.value);

                    // 1-2. round_time 예약 가능 시간대 확인
                    console.log(round_time.value);

                    // 1-4. 인원 최소, 최대값 범위 확인
                    console.log(pax.value);

                    // 1-4. 카트 수량 최소, 최대값 범위 확인
                    // 1-5. 카트 의무
                    console.log(cart.value);

                    // 2. 견적 계산
                }
            });
        });
    });
