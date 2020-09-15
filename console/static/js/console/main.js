document.addEventListener('DOMContentLoaded', () => {

    const navbarTop = document.getElementById('navbar-top');

    window.addEventListener('scroll', function (e) {
        if ((window.scrollY || document.documentElement.scrollTop) > 20) {
            navbarTop.style.boxShadow = "0 10px 5px -2px rgba(0,0,0,0.2)";
            navbarTop.style.transitionDuration = "0.1s";
        } else {
            navbarTop.style.boxShadow = "none";
            navbarTop.style.transitionDuration = "inherit";
        }
    });

    runApp();
});