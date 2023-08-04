$(document).ready(function () {

    // Default to Text Input
    $("#div-textarea").show()
    $("#div-url").hide()
    $("#div-media").hide()

    // Show and Hide DIVs based on button click.
    $("#btn-prompt-text").click(() => {
        $("#div-textarea").show()
        $("#div-url").hide()
        $("#div-media").hide()
    });
    $("#btn-prompt-url").click(() => {
        $("#div-textarea").hide()
        $("#div-url").show()
        $("#div-media").hide()
    });
    $("#btn-prompt-media").click(() => {
        $("#div-textarea").hide()
        $("#div-url").hide()
        $("#div-media").show()
    });

    // Form Submit and Show Overlay.
    $("#btn-find-sentiment").click((e) => {
        e.preventDefault();

        let input = ""
        if ($("#div-textarea").is(":visible")) {
            input = $("#form-input-textarea").val();
            type = "text";
        } else if ($("#div-url").is(":visible")) {
            input = $("#form-input-url").val();
            type = "url";
        } else if ($("#div-media").is(":visible")) {
            input = $("#form-input-media").val();
            type = "media";
        }

        if (input != '') {
            $("#overlay").css("display", "block");
            $.ajax({
                type: "POST",
                url: '/',
                data: JSON.stringify({
                    "input": input,
                    "type": type
                }),
                dataType: 'json',
                contentType: 'application/json'
            })
                .done((response) => {
                    console.log(response)
                    val_neg = Math.round(parseFloat(response["score_negative"]) * 10000) / 100
                    val_neu = Math.round(parseFloat(response["score_neutral"]) * 10000) / 100
                    val_pos = Math.round(parseFloat(response["score_positive"]) * 10000) / 100
                })
        }

    })

})