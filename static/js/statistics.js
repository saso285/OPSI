$(document).ready(function () {

    var selectorTypePercentage = $('#typePercentageChart');
    var selectorErrorPercentage = $('#errorPercentageChart');

    function ajaxGetHttpRequest(url) {
        var response;
        $.ajax({
            type: 'GET',
            url: url,
            contentType: 'application/json',
            dataType: 'json',
            async: false,
            success: function (res) {
                response = res.result;
            },
            error: function (res) {
                console.log(res);
            }
        });
        return response;
    }

    function setOptions(name, data) {
        return {
            title: {
                text: name
            },
            data: [{
                type: "pie",
                startAngle: 30,
                showInLegend: "true",
                legendText: "{label}",
                indexLabel: "{label} ({y})",
                yValueFormatString: "#,##0.#" % "",
                dataPoints: data
            }]
        };
    }

    selectorTypePercentage.CanvasJSChart(setOptions(
        "Data type occurrence percentage",
        ajaxGetHttpRequest('/statistics/types')
    ));
    selectorErrorPercentage.CanvasJSChart(setOptions(
        "Error occurrence percentage",
        ajaxGetHttpRequest('/statistics/error')
    ));

});