
$("#next-card").on("click", function() {
    console.log('hello')
    $url = $('#next-card-url').data('url');
    $.ajax({
        type: "get",
        url: $url,
        // data: "data",
        success: ShowCard,
    });
})


function ShowCard(response) {
    if (response.expired === true) {
        window.location.replace(response.redirect)
    }
    else {
        $('#card_content').empty();
        $('#card_content').html(response.html)
    }

}


$("#check-result").on("click", function() {
    $url = $('#check-card-url').data('url');
    $.ajax({
        type: "post",
        url: $url,
        data: $('#form-check-result').serialize(),
        success: ShowResult,
    });
})


function ShowResult(response) {
    console.log(response.data)
    $('#card_content').empty();
    $('#card_content').html(response.html);
}


$("#btn-end").on("click", function() {
    console.log('hello')
    $url = $('#study-end-url').data('url');
    $.ajax({
        type: "get",
        url: $url,
        // data: "data",
        success: ShowCard,
    });
})