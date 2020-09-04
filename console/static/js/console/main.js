document.addEventListener('DOMContentLoaded', () => {
    document
        .getElementById('burger-icon')
        .addEventListener('click', function (e) {
            const left_sidebar = document.getElementById('left-sidebar');

            if (left_sidebar.classList.contains('is-hidden-mobile')) {
                left_sidebar.classList.remove('is-hidden-mobile');
            } else {
                left_sidebar.classList.add('is-hidden-mobile');
            }
        });
});