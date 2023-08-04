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

})