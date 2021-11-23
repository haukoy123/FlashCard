
$("#id_avatar").on('change', function() {
    $element = $(this);
    var reader = new FileReader();
    reader.onload = function(e) {
        $("#get_avatar")[0].src = e.target.result;
    };
    reader.readAsDataURL($element[0].files[0]);

});




// {% if login_form.errors %}
// <script>
//     $(document).ready(function(){
//         $("#LoginModal").modal('show');
//     });
// </script>
// {% endif %}
// {% if register_form.errors %}
// <script>
//     $(document).ready(function(){
//         $("#RegisterModal").modal('show');
//     });
// </script>
// {% endif %}
