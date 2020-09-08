function runApp() {
    const search = document.getElementById('id_search');
    const keyword = document.getElementById('id_keyword');

    keyword.type = 'date';

    search.addEventListener('change', function (e) {
        console.log('changed');
        console.log(this.value);

        if (this.value === 'round_date') {
            keyword.type = 'date';
            keyword.value = '';
            keyword.placeholder = 'HH:MM';
        } else if (this.value === 'customer') {
            keyword.type = 'text';
            keyword.value = '';
            keyword.placeholder = 'Customer name';
        }
    });
}
