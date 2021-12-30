
$("#next-card").on("click", function() {
    $url = $('#next-card-url').data('url');
    $.ajax({
        type: "get",
        url: $url,
        // data: "data",
        success: ShowCard,
        error: function () {
            alert("Yêu cầu thất bại!\nBạn vui lòng đăng nhập lại để sử dụng tiếp.\nHãy liên hệ với chúng tối nếu bạn vẫn xảy ra trường hợp này.");
        }
    });
})


function ShowCard(response) {
    // console.log(response.card.card)
    $('#card_content').empty();
    $('#card_content').html(response.html);
    $('.txt_keyboard_events').focus();
}


$("#check-result").on("click", function() {
    $url = $('#check-card-url').data('url');
    $.ajax({
        type: "post",
        url: 'http://127.0.0.1:8000/cardgroups/25/study/gsdfgd/',
        data: $('#form-check-result').serialize(),
        success: ShowResult,
        error: function () {
            alert("Yêu cầu thất bại!\nBạn vui lòng đăng nhập lại để sử dụng tiếp.\nHãy liên hệ với chúng tối nếu bạn vẫn xảy ra trường hợp này.");
        }
    });
})


function ShowResult(response) {
    console.log(response.data)
    $('#card_content').empty();
    $('#card_content').html(response.html);
    $('.txt_keyboard_events').focus();
    $('.txt_keyboard_events').popover('show');
}


$("#confirm-end-study").on("click", function() {
    $url = $('#end-study-url').data('url');
    $.ajax({
        type: "get",
        url: $url,
        // data: "data",
        success: ShowCard,
        error: function () {
            alert("Yêu cầu thất bại!\nBạn vui lòng đăng nhập lại để sử dụng tiếp.\nHãy liên hệ với chúng tối nếu bạn vẫn xảy ra trường hợp này.");
        }
    });
    $('#modal-end-study').modal('hide');
})


$('.txt_keyboard_events').on('keydown',function (e) {
    if (e.ctrlKey && e.keyCode == 13) {
        const check_result = $('#check-result');
        if(check_result.length===1){
            check_result.click();
        }
        else{
            const next_card = $('#next-card');
            if(next_card.length===1){
                next_card.click();
            }
        }
    }
});


$(".txt_keyboard_events").on("keydown", function(){
    $(this).popover('show');
});
