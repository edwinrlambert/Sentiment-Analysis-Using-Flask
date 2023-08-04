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

        let formData = new FormData();

        if ($("#div-textarea").is(":visible")) {
            formData.append("input", $("#form-input-textarea").val());
            formData.append("type", "text")
        } else if ($("#div-url").is(":visible")) {
            formData.append("input", $("#form-input-url").val());
            formData.append("type", "url")
        } else if ($("#div-media").is(":visible")) {
            formData.append("input", $("#form-input-media")[0].files[0]);
            formData.append("type", "media")
        }

        if (formData.get("input") != '') {
            $("#sentiment-overlay").css("display", "block");
            $.ajax({
                type: "POST",
                url: '/',
                data: formData,
                dataType: 'json',
                contentType: false,
                processData: false,
            })
                .done((response) => {
                    val_neg = Math.round(parseFloat(response["score_negative"]) * 10000) / 100
                    val_neu = Math.round(parseFloat(response["score_neutral"]) * 10000) / 100
                    val_pos = Math.round(parseFloat(response["score_positive"]) * 10000) / 100

                    $("#sentiment-overlay-content").html(`
                        <h2>PROMINENT SENTIMENT</h2>
                        <p id="prominent-sentiment">` + response["prominent_sentiment"] + `</p>
                        <div id="sentiment-info">
                            <div id="sentiment-table">
                                <table class="table">
                                    <thead>
                                        <th scope="col">&#128566;</th>
                                        <th scope="col">SENTIMENT</th>
                                        <th scope="col">VALUE</th>
                                    </thead>
                                    <tbody>
                                        <tr>
                                            <td>&#128543;</td>
                                            <td>Negative</td>
                                            <td>` + val_neg + `%</td>
                                        </tr>
                                        <tr>
                                            <td>&#128528;</td>
                                            <td>Neutral</td>
                                            <td>` + val_neu + `%</td>
                                        </tr>
                                        <tr>
                                            <td>&#128512;</td>
                                            <td>Positive</td>
                                            <td>` + val_pos + `%</td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                            <canvas id="sentiment-radar-chart"></canvas>
                        </div>
                    `)

                    const chart = $("#sentiment-radar-chart")
                    new Chart(chart, {
                        type: 'radar',
                        data: {
                            labels: ['Negative', 'Neutral', 'Positive'],
                            datasets: [{
                                label: 'Sentiment',
                                data: [val_neg, val_neu, val_pos],
                                fill: true,
                                color: '#FFFFFF',
                                backgroundColor: 'rgba(255, 99, 132, 0.5)',
                                borderColor: 'rgb(255, 99, 132)',
                                pointBackgroundColor: '#FFFFFF',
                                pointBorderColor: '#FFFFFF',
                                pointHoverBackgroundColor: '#FFFFFF',
                                pointHoverBorderColor: '#FFFFFF'
                            }]
                        },
                        options: {
                            elements: {
                                line: {
                                    borderWidth: 5
                                },
                                legend: {
                                    labels: {
                                        color: 'rgb(255, 255, 255)',
                                        fontSize: 18
                                    }
                                }
                            },
                            scales: {
                                r: {
                                    angleLines: {
                                        color: 'rgba(255, 255, 255, 0.8)'
                                    },
                                    grid: {
                                        color: 'rgba(255, 255, 255, 0.8)'
                                    },
                                    pointLabels: {
                                        color: 'rgb(255, 255, 255)',
                                        fontSize: 20
                                    },
                                    ticks: {
                                        color: 'rgb(0, 0, 0)'
                                    }
                                }
                            }
                        }
                    });
                })
                .fail((err) => {
                    console.log(err)
                })
        }

    });

    // Remove overlay
    $("#sentiment-overlay").click(() => {
        $("#sentiment-overlay").css("display", "none");
        $("#form-input-textarea").val("");
        $("#form-input-url").val("");
        $("#form-input-media").val("");
        window.location.reload()
    });

});