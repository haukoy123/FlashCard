$(document).ready(function(){
    if ($(".messages").length != 0){
        $("#liveToast").toast('show');
    }
});

$(".dropdown").hover(function(){
    $(".dropdown-menu").toggle();
})
