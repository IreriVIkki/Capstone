$(document).ready(function () {
    var $newItemForm = $('.js-new-item')

    $newItemForm.submit(function (event) {
        console.log('submited')
        event.preventDefault()
        var $formData = $(this).serialize()
        var $thisURL = $newItemForm.attr('data-url') || window.location.href
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
        var $testContent = $('.js_update_items')
        $testContent.html(info)
        console.log(info)
    }

    function handleFormError(jqXHR, textStatus, errorThrown) {
        console.log(jqXHR)
        console.log(textStatus)
        console.log(errorThrown)
    }
})