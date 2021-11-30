$(document).ready(function(){
    $("#LoginModal").modal('show');
    if ($("#RegisterModal .errorlist").length != 0){
        $("#RegisterModal").modal('show');
    }
    else if ($("#LoginModal .errorlist").length != 0){
        $("#LoginModal").modal('show');
    }
});

$("#id_avatar").on('change', function() {
    $element = $(this);
    var reader = new FileReader();
    reader.onload = function(e) {
        $("#image")[0].src = e.target.result;
    };
    reader.readAsDataURL($element[0].files[0]);
});
