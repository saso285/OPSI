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
            color: '#5182ba', width: 6
        },
        to: {
            color: '#5182ba', width: 6
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
    var selectorDatasetNum = $('#datasetNum');
    var selectorErrorCount = $('#errorCount');
    var selectorAllData = $('#allData');
    var selectorTransformedData = $('#transformedData');
    var bar = progresBarCircle();

    bar.text.style.fontFamily = '"Raleway", Helvetica, sans-serif';
    bar.text.style.fontSize = '3rem';

    selectorFieldsChart.hide();

    function setOptionsPieChart(name, data, type, indexLabel) {
        return {
            title: {
                text: name,
                fontFamily: "tahoma",
            },
            data: [{
                type: type,
                startAngle: 30,
                indexLabel: indexLabel,
                yValueFormatString: "#,##0.#" % "",
                dataPoints: data
            }]
        };
    }

    selectorTypePercentage.CanvasJSChart(setOptionsPieChart(
        "Transformed data type count",
        ajaxGetHttpRequest('/statistics/types'),
        "bar",
        "{y}"
    ));
    selectorErrorPercentage.CanvasJSChart(setOptionsPieChart(
        "Error occurrence percentage while performing data pull",
        ajaxGetHttpRequest('/statistics/error'),
        "pie",
        "{label} ({y}%)"
    ));
    selectorUnknownExtensionsCount.CanvasJSChart(setOptionsPieChart(
        "Transformation error by type",
        ajaxGetHttpRequest('/statistics/extension'),
        "pie",
        "{label} ({y})"
    ));

    var percentage = ajaxGetHttpRequest('/statistics/percentage');
    selectorDatasetNum.text("Complete count: " + percentage.dataset_num)
    selectorErrorCount.text("Error count: " + percentage.error_count)

    var percentage = ajaxGetHttpRequest('/statistics/countData');
    selectorAllData.text("All files: " + percentage.all)
    selectorTransformedData.text("Transformed files: " + percentage.accessible)

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
            "pie",
            true
        ));
        selectorFieldsChart.show();
    });

});