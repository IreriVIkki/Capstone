$(document).ready(function () {
    $('#js-new-question').submit(function (e) {
        e.preventDefault();
        var form = $(this);
        var html_update = String()
        $.ajax({
            type: form.attr('method'),
            url: form.attr('action'),
            dataType: 'text',
            data: form.serialize(),
            success: function (data) {
                data = JSON.parse(data)
                if (data.form_is_valid) {
                    $('.js_update_questions').html(data.home_update);
                }
            }
        });
    });
    return false;
});