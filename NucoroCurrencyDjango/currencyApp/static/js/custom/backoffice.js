$(document).ready(function() {
    $('#source_currency').select2({

    });
});


function getRandomColor() {
    var r = Math.floor(Math.random() * 255);
    var g = Math.floor(Math.random() * 255);
    var b = Math.floor(Math.random() * 255);
    return "rgb(" + r + "," + g + "," + b + ")";
 };


function drawGraph(labels, datasets){
    var ctx = document.getElementById('exchange-rate-evolution').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: datasets
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
}


function parseAPIData(data){
    var datasets = []
    var counter = 0;
    var labels = [];
    for (var i in data){
        var data_row = [];
        for (var j in data[i]){
            if (counter < 1){
                labels.push(j);
            }
            data_row.push(data[i][j])
        }
        datasets.push({
            label: i,
            data: data_row,
            borderColor: getRandomColor(),
            fill: false
        });
        counter += 1;
    }
    
    return [labels, datasets];
}



function getGraph(mockdata=null){
    if (mockdata !== null){
        var results = parseAPIData(mockdata);
        drawGraph(results[0], results[1]);
    } else {
        var x = $('#backoffice-form').serializeArray();
        var data = {};
        var form_ready = true;
        $.each(x, function(i, field){
            data[field.name] = field.value;
            if (field.value === ''){
                form_ready = false;
            }
        });
        var full_url = '/timeseries/?' + $.param(data);

        if (form_ready){
            fetch(full_url)
            .then(response => response.json())
            .then(data => {
                var results = parseAPIData(data);
                drawGraph(results[0], results[1]);
        })};
    
    }
}


