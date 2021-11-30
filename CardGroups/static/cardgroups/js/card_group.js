$(".card-group").hover(function() {
    $(this).css({
        "margin": "0px",
        "box-shadow": "5px 5px #ffeb3b, 10px 10px #4caf50, 15px 15px #ff57229e, 20px 20px 5px #2f2f2f"
    })
},function() {
    $(this).css({
        "margin": "5px",
        "box-shadow": "3px 3px #ffeb3b, 6px 6px #4caf50, 9px 9px #ff57229e, 12px 12px 5px #2f2f2f"
    })
});

$(".create-group").hover(function() {
    $(this).css({
        'color': 'white',
        "box-shadow": "6px 6px 5px #2f2f2f"
    })
},
function() {
    $(this).css({
        'color': 'white',
        "box-shadow":'none'
    })
})