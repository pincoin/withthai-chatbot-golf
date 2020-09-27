function setSearchKeyword(search, keyword) {
    if (search.value === 'round_date') {
        keyword.type = 'date';
        keyword.value = '';
        keyword.placeholder = 'HH:MM';
    } else if (search.value === 'customer_name') {
        keyword.type = 'text';
        keyword.value = '';
        keyword.placeholder = 'Customer name';
    }
}

function runApp() {
    const search = document.getElementById('id_search');
    const keyword = document.getElementById('id_keyword');

    if (search.value === 'round_date') {
        keyword.type = 'date';
        keyword.placeholder = 'HH:MM';
    } else if (search.value === 'customer_name') {
        keyword.type = 'text';
        keyword.placeholder = 'Customer name';
    }

    search.addEventListener('change', function (e) {
        setSearchKeyword(search, keyword);
    });

    const order_status = document.getElementById('id_order_status');
    const payment_status = document.getElementById('id_payment_status');
    const sort = document.getElementById('id_sort');

    [order_status, payment_status, sort].forEach(function (element) {
        element.addEventListener('change', function (e) {
            this.form.submit();
        });
    });

    console.log(gettext('translated'));
}
