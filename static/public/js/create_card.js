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



// $('.input_card').change(function(){
//     const $elements = $('.input_card');
//     const btn = get_btn($elements)
//     if (btn === 'btn_done'){
//         $('#btn_done').show();
//         $('#link_done').hide();
//     }
//     else {
//         $('#btn_done').hide();
//         $('#link_done').show();
//     }

//     // console.log('hello')
// });


// function get_btn(elements) {
//     elements.each(function() {
//         const $element = $(this)
//         if ($element[0].value != ''){
//             return 'btn_done'
//         }
//         return 'link_done'
//     })
// }


