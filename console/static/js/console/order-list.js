function setSearchKeyword(search, keyword) {
    if (search.value === 'round_date') {
        keyword.type = 'date';
        keyword.value = '';
        keyword.placeholder = 'HH:MM';
    } else if (search.value === 'customer') {
        keyword.type = 'text';
        keyword.value = '';
        keyword.placeholder = 'Customer name';
    }
}

function runApp() {
    const search = document.getElementById('id_search');
    const keyword = document.getElementById('id_keyword');

    setSearchKeyword(search, keyword);

    search.addEventListener('change', function (e) {
        console.log('changed');
        console.log(this.value);

        setSearchKeyword(search, keyword);
    });
}
