document.addEventListener('DOMContentLoaded', () => {
    const navbarTop = document.getElementById('navbar-top');

    const leftSidebar = document.getElementById('left-sidebar');
    const leftSidebarClose = document.getElementById('left-sidebar-close');
    const leftSidebarModalBackground = document.querySelector('#left-sidebar .modal-background');

    const rightSidebar = document.getElementById('right-sidebar');
    const rightSidebarClose = document.getElementById('right-sidebar-close');
    const rightSidebarModalBackground = document.querySelector('#right-sidebar .modal-background');

    // Top navbar box shadow when scrolled down
    window
        .addEventListener('scroll', function (e) {
            if ((window.scrollY || document.documentElement.scrollTop) > 20) {
                navbarTop.style.boxShadow = "0 10px 5px -2px rgba(0,0,0,0.2)";
                navbarTop.style.transitionDuration = "0.1s";
            } else {
                navbarTop.style.boxShadow = "none";
                navbarTop.style.transitionDuration = "inherit";
            }
        });

    // Open left sidebar
    document
        .getElementById('left-sidebar-open')
        .addEventListener('click', function (e) {
            document.documentElement.classList.add('is-clipped');
            leftSidebar.classList.add('is-active');
        });

    // Close left sidebar
    [leftSidebarClose, leftSidebarModalBackground,].forEach(element => {
        element
            .addEventListener('click', function (e) {
                leftSidebar.classList.remove('is-active');
                document.documentElement.classList.remove('is-clipped');
            });
    });

    // Open right sidebar
    document
        .getElementById('right-sidebar-open')
        .addEventListener('click', function (e) {
            document.documentElement.classList.add('is-clipped');
            rightSidebar.classList.add('is-active');
        });

    // Close right sidebar
    [rightSidebarClose, rightSidebarModalBackground,].forEach(element => {
        element
            .addEventListener('click', function (e) {
                rightSidebar.classList.remove('is-active');
                document.documentElement.classList.remove('is-clipped');
            });
    });

    runApp();
});