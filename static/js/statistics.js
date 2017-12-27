function progresBarCircle() {
    return new ProgressBar.Circle(container, {
        color: '#aaa',
        strokeWidth: 6,
        trailWidth: 1,
        easing: 'easeInOut',
        duration: 1400,
        text: {
            autoStyleContainer: false
        },
        from: {
            color: '#b54d4d', width: 6
        },
        to: {
            color: '#9cba5e', width: 6
        },
        step: function (state, circle) {
            circle.path.setAttribute('stroke', state.color);
            circle.path.setAttribute('stroke-width', state.width);
            var value = Math.round(circle.value() * 100);
            if (value === 0) {
                circle.setText('0%');
            } else {
                circle.setText(value + "%");
            }
        }
    });
}

$(document).ready(function () {

    var selectorTypePercentage = $('#typePercentageChart');
    var selectorErrorPercentage = $('#errorPercentageChart');
    var selectorUnknownExtensionsCount = $('#unknownExtensionChart');
    var bar = progresBarCircle();

    bar.text.style.fontFamily = '"Raleway", Helvetica, sans-serif';
    bar.text.style.fontSize = '3rem';

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
                console.log(res);
                console.log(response);
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
                text: name,
                fontFamily: "tahoma",
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
        "Data type count",
        ajaxGetHttpRequest('/statistics/types')
    ));
    selectorErrorPercentage.CanvasJSChart(setOptions(
        "Error occurrence percentage",
        ajaxGetHttpRequest('/statistics/error')
    ));
    selectorUnknownExtensionsCount.CanvasJSChart(setOptions(
        "Unknown extension count",
        ajaxGetHttpRequest('/statistics/extension')
    ));
    bar.animate(ajaxGetHttpRequest('/statistics/accessible'));

});