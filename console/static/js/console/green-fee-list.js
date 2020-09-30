let runApp = function () {
    const seasons = document.getElementById('id_seasons');
    const day_of_week = document.getElementById('id_day_of_week');
    const timeslots = document.getElementById('id_timeslots');
    const customer_groups = document.getElementById('id_customer_groups');

    [seasons, day_of_week, timeslots, customer_groups].forEach(function (element) {
        element.addEventListener('change', function (e) {
             this.form.submit();
        });
    });
}