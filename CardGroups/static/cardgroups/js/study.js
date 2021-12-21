
$("#next-card").on("click", function() {
    $url = $('#next-card-url').data('url');
    $.ajax({
        type: "get",
        url: $url,
        // data: "data",
        success: ShowCard,
    });
})


function ShowCard(response) {
    // console.log(response.card.card)
    $('#card_content').empty();
    $('#card_content').html(response.html);
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


$("#confirm-end-study").on("click", function() {
    console.log('hello2')
    $url = $('#end-study-url').data('url');
    $.ajax({
        type: "get",
        url: $url,
        // data: "data",
        success: ShowCard,
    });
    $('#modal-end-study').modal('hide');
})