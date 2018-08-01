function set_pagination_btn(b_id, url){
    let button = $('#' + b_id);
    url ? button.data('href', url).removeClass('disabled') : button.addClass('disabled');
}

function get_stores_table(url) {
    if (!url) return false;

    $.get(url, {}, function (data) {
        if (data['detail']) {
            window.location.href = '/';
        }
        else {
            if (!data['results'].length) {
                $('#stores_table').hide();
                $('#no_results_found').show();
                return;
            }
            else {
                $('#stores_table').show();
                $('#no_results_found').hide();
            }
            const number = (data['page'] - 1) * data['per_page'] + 1;
            let tbody = $('#table_rows');
            for (let i = 0; i < data['results'].length; i++) {
                let tr_obj = $('<tr>');
                tr_obj.append($('<td>', {text: number + i}));
                tr_obj.append($('<td>').append($('<a>', {text: data['results'][i]['name'], href: data['results'][i]['url']})));
                tr_obj.append($('<td>', {text: new Date(Date.parse(data['results'][i]['date_created']))}));
                tr_obj.append($('<td>', {text: new Date(Date.parse(data['results'][i]['date_changed']))}));
                i === 0 ? tbody.html(tr_obj) : tbody.append(tr_obj);
            }
            $('#curr_page').text(data['page']);
            $('#total_pages').text(data['num_pages']);
            $('#total_objs_number').text(data['count']);
            set_pagination_btn('first_page', data['links']['first']);
            set_pagination_btn('prev_page', data['links']['previous']);
            set_pagination_btn('next_page', data['links']['next']);
            set_pagination_btn('last_page', data['links']['last']);
        }
    }).fail(function () { window.location.href = '/' });
}

$(document).ready(function () {
    let page_api_url = '/shop-api/stores/';
    get_stores_table(page_api_url);
    $('#stores_table').show();

    $('.pagination-btn').click(function () {
        get_stores_table($(this).data('href'));
    });

    $('#search_form').find('input').keyup(function (event) {
        if (event.keyCode === 13) {
            let search_url = page_api_url;
            const search_val = $(this).val();
            if (search_val.length) search_url += '?name=' + encodeURIComponent(search_val);
            get_stores_table(search_url);
        }
    })
});