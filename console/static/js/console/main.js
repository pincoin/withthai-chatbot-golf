document.addEventListener('DOMContentLoaded', () => {
    const navbarTop = document.getElementById('navbar-top');

    const leftSidebar = document.getElementById('left-sidebar');
    const leftSidebarModalBackground = document.querySelector('#left-sidebar .modal-background');

    const rightSidebar = document.getElementById('right-sidebar');
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
            /*
            leftSidebar.animate([
                {left: '0%'},
            ], {
                duration: 150,
            });
             */
        });

    // Close left sidebar
    [leftSidebarModalBackground,].forEach(element => {
        element
            .addEventListener('click', function (e) {
                leftSidebar.classList.remove('is-active');
                /*
                leftSidebar.animate([
                    {left: '-1000%'},
                ], {
                    duration: 150,
                });
                 */
                document.documentElement.classList.remove('is-clipped');
            });
    });

    // Open right sidebar
    document
        .getElementById('right-sidebar-open')
        .addEventListener('click', function (e) {
            document.documentElement.classList.add('is-clipped');
            rightSidebar.classList.add('is-active');
            /*
            rightSidebar.animate([
                {right: '0%'},
            ], {
                duration: 150,
            });
             */
        });

    // Close right sidebar
    [rightSidebarModalBackground,].forEach(element => {
        element
            .addEventListener('click', function (e) {
                rightSidebar.classList.remove('is-active');
                /*
                rightSidebar.animate([
                    {right: '-1000%'},
                ], {
                    duration: 150,
                });
                 */
                document.documentElement.classList.remove('is-clipped');
            });
    });

    runApp();
});