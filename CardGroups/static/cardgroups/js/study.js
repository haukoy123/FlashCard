
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
        $('#id_back').val('')
        $('#id_front').val(response.card.card.front)
    
        $("#show-result").empty();
        const txt = $("<span></span>").addClass('fw-bold').text('Nhấn kiểm tra để xem kết quả')
        $("#show-result").append(txt);
    
        $("#check-result").show();
        $("#next-card").hide();
    
        $("#id_back").focus();
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
    const txt = $("<span></span>").addClass('fw-bold text-success h5').text('Tuyệt vời. Bạn ghi nhớ rất tốt')
    const restult = $("<span></span>").html("<small class='fw-bold h6'>Đáp án: </small>" + response.card.back)

    if (response.result === false) {
        txt.addClass('text-danger').text('Kết quả chưa chính xác')
    }
    $("#show-result").empty();
    $("#show-result").append(txt, "<br>", restult)

    $("#check-result").hide();
    $("#next-card").show();

    // $("#btn").empty();
    // const btn_next_card = $("<button></button").addClass('btn btn-primary w-75').attr({'type': 'button', 'id': 'next-card'}).text('Tiếp tục');
    // $("#btn").append(btn_next_card)
    // $("#next-card").on("click", function() {
    //     console.log('hello')
    //     $url = $('#next-card-url').data('url');
    //     $.ajax({
    //         type: "get",
    //         url: $url,
    //         // data: "data",
    //         success: ShowCard,
    //     });
    // })
}


