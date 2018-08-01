function set_initial_dates() {
    $('input[data-type="date"]').each(function () {
        const initial_date = $(this).data('value');
        if (initial_date) $(this).closest('.ui.calendar').calendar('set date', new Date(Date.parse(initial_date)));
    });
}

$(document).ready(function () {
    $('.ui.calendar').calendar();

    $('.pagination-btn').click(function () {
        window.location.href = get_url_with_get_parameter(window.location.href, 'page', $(this).data('page'));
    });
    $('#reset_filters').click(function (event) {
        event.preventDefault();
        window.location.href = window.location.pathname;
    });
    $('.ui.dropdown').dropdown({placeholder: ""});
    set_initial_dates();
});