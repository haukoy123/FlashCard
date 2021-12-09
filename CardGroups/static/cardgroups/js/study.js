
$("#next-card").on("click", function() {
    $.ajax({
        type: "get",
        url: "http://127.0.0.1:8000/cardgroups/22/study/continue/",
        // data: "data",
        success: ShowCard,
    });
})


function ShowCard(response) {
    console.log(response.card)
}


$("#check-result").on("click", function() {
    $.ajax({
        type: "get",
        url: "http://127.0.0.1:8000/cardgroups/22/study/check/",
        data: {
            back: $("#id_back").val(),
        },
        success: ShowResult,
    });
})


function ShowResult(response) {

}