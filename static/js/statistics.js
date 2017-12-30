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

function ajaxPostHttpRequest(url, data) {
    var response;
    $.ajax({
        type: 'POST',
        url: url,
        contentType: 'application/json',
        dataType: 'json',
        data: JSON.stringify(data),
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

$(document).ready(function () {

    var selectorTypePercentage = $('#typePercentageChart');
    var selectorErrorPercentage = $('#errorPercentageChart');
    var selectorUnknownExtensionsCount = $('#unknownExtensionChart');
    var selectorFieldsList = $('#fieldsList');
    var selectorFieldsChart = $('#fieldsChart');
    var bar = progresBarCircle();

    bar.text.style.fontFamily = '"Raleway", Helvetica, sans-serif';
    bar.text.style.fontSize = '3rem';

    selectorFieldsChart.hide();

    function setOptionsPieChart(name, data, type) {
        return {
            title: {
                text: name,
                fontFamily: "tahoma",
            },
            data: [{
                type: type,
                startAngle: 30,
                showInLegend: "true",
                legendText: "{label}",
                indexLabel: "{label} ({y})",
                yValueFormatString: "#,##0.#" % "",
                dataPoints: data
            }]
        };
    }

    selectorTypePercentage.CanvasJSChart(setOptionsPieChart(
        "Data type count",
        ajaxGetHttpRequest('/statistics/types'),
        "bar"
    ));
    selectorErrorPercentage.CanvasJSChart(setOptionsPieChart(
        "Error occurrence percentage",
        ajaxGetHttpRequest('/statistics/error'),
        "pie"
    ));
    selectorUnknownExtensionsCount.CanvasJSChart(setOptionsPieChart(
        "Unknown extension count",
        ajaxGetHttpRequest('/statistics/extension'),
        "pie"
    ));
    bar.animate(ajaxGetHttpRequest('/statistics/accessible'));
    ajaxGetHttpRequest('/fields').forEach(function(elem) {
        var aHref = '<option value="' + elem + '">' + elem + '</a>';
        selectorFieldsList.append(aHref);
    });
    selectorFieldsList.change(function(elem) {
        var field = selectorFieldsList.find(":selected").text();
        selectorFieldsChart.CanvasJSChart(setOptionsPieChart(
            "Field statistics",
            ajaxPostHttpRequest('/statistics/field', {'field': field}),
            "pie"
        ));
        selectorFieldsChart.show();
    });

});