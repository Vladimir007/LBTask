function set_initial_dates() {
    $('input[data-type="date"]').each(function () {
        const initial_date = $(this).data('value');
        if (initial_date) $(this).closest('.ui.calendar').calendar('set date', new Date(Date.parse(initial_date)));
    });
}

function add_product_number_field(p_id, p_val, text) {
    $('#products_numbers').append(
        $('<div>', {'class': 'field', id: 'product_number_' + p_id})
            .append($('<label>', {text: text, for: 'product-number-' + p_id}))
            .append($('<input>', {name: 'product-number-' + p_id, type: 'number', min: '1', step: '1', value: p_val}))
    );
}

function set_initial_values() {
    set_initial_dates();

    let products_input = $('#products_input');
    $.each(products_input[0].attributes, function (i, a) {
        if (a.name.startsWith('data-number-')) {
            let p_id = a.name.replace('data-number-', ''), p_val = a.value,
                text = products_input.find('option[value="' + p_id + '"]').text();
            add_product_number_field(p_id, p_val, text);
        }
    });
}

$(document).ready(function () {
    $('.ui.calendar').calendar();
    $('.ui.dropdown').dropdown();

    $('#products_input').closest('.ui.dropdown').dropdown({
        onAdd: function (val, text) { add_product_number_field(val, '1', text) },
        onRemove: function (val) { $('#product_number_' + val).remove() }
    });
    set_initial_values();

    // Semantic ui form validation
    $('.ui.form').form({
        fields: {
            doc_type: {identifier: 'doc_type', rules: [{type   : 'empty', prompt : 'Please choose document type'}]},
            store: {identifier: 'store', rules: [{type   : 'empty', prompt : 'Please choose document store'}]},
            products: {identifier: 'products', rules: [{type   : 'minCount[1]', prompt : 'Please select at list one product'}]},
            doc_date: {identifier: 'doc_date', rules: [{type   : 'empty', prompt : 'Please set document date'}]}
        }
    });

    // Disable default validation and add semantic ui validation on form submit
    $('form').attr('novalidate', true).submit(function () {
        let ui_form = $('.ui.form');
        ui_form.form('validate form');
        return ui_form.form('is valid');
    });
});