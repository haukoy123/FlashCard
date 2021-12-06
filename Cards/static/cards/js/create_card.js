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
