$(document).ready(function () {
    var $myForm = $('.my-ajax-form')
    $myForm.submit(function (event) {
        event.preventDefault()
        var $formData = $(this).serialize()
        var $thisURL = $myForm.attr('data-url') || window.location.href
        console.log($thisURL)
        $.ajax({
            method: "POST",
            url: $thisURL,
            data: $formData,
            success: handleFormSuccess,
            error: handleFormError,
        })
    })

    function handleFormSuccess(info, textStatus, jqXHR) {
        console.log(info)
        var $testContent = $('.js-test-content')
        $testContent.html(info)
        console.log(jqXHR)
        console.log(textStatus)
    }

    function handleFormError(jqXHR, textStatus, errorThrown) {
        console.log(jqXHR)
        console.log(textStatus)
        console.log(errorThrown)
    }
})