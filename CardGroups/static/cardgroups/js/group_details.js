$(document).ready(function(){
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl)
    })
})


$('.btn-edit').on('click', function() {
    $('#group-details').hide();
    $('#edit-group').show();
})

$('.btn-close').on('click', function() {
    $('#group-details').show();
    $('#edit-group').hide();
})
