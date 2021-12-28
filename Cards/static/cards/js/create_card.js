$('.input_card').change(function(){
    const $elements = $('.input_card');
    let display = 'link_done';
    $elements.each(function() {
        const $element = $(this)
        if ($element[0].value != ''){
            display = 'btn_done';
        }
    });
    if (display === 'link_done') {
        $('#link_done').show();
        $('#btn_done').hide();
        
    }
    else{
        $('#link_done').hide();
        $('#btn_done').show();
    }
});


$(".input_card").on("keydown", function(){
    $(this).popover('show');
});


$('.input_card').on('keydown',function (e) {
    const $elements = $('.input_card');
    let $link_or_btn_done = 'link_done';
    $elements.each(function() {
        const $element = $(this)
        if ($element[0].value != ''){
            $link_or_btn_done = 'btn_done';
        }
    });
    
    if (e.ctrlKey && e.keyCode == 13) {
        if ($link_or_btn_done === 'link_done') {
            $('#link_done')[0].click();
            
        }
        else{
            $('#btn_done').click();
        }
    }

    if (e.altKey && e.keyCode == 13) {
        $('#btn_continue').click()
    }
});
