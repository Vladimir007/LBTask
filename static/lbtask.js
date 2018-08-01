function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            const csrftoken = getCookie('csrftoken');
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$.extend({
    redirectPost: function (location, args) {
        let form = '<input type="hidden" name="csrfmiddlewaretoken" value="' + getCookie('csrftoken') + '">';
        $.each(args, function (key, value) {
            form += '<input type="hidden" name="' + key + '" value=\'' + value + '\'>';
        });
        $('<form action="' + location + '" method="POST">' + form + '</form>').appendTo($(document.body)).submit();
    }
});

window.get_url_with_get_parameter = function (url, key, value) {
    if (url.indexOf(key + '=') > -1) {
        let url_regex = new RegExp('(' + key + "=).*?(&|$)");
        return url.replace(url_regex, '$1' + value + '$2');
    }
    else if (url.indexOf('?') > -1) {
        return url + '&' + key + '=' + value;
    }
    else {
        return url + '?' + key + '=' + value;
    }
};

$(document).ready(function () {
    $('#logout').click(function (event) {
        event.preventDefault();
        $.post('/logout/', {}, function (resp) {
            window.location.href = '/login/';
        });
    });
});
