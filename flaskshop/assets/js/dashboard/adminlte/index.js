import 'jquery-sparkline';

import Chart from 'chart.js';

// This will get the first returned node in the jQuery collection.
var salesChartData = {
    labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
    datasets: [
        {
            label: 'Electronics',
            fillColor: '#dee2e6',
            strokeColor: '#ced4da',
            pointColor: '#ced4da',
            pointStrokeColor: '#c1c7d1',
            pointHighlightFill: '#fff',
            pointHighlightStroke: 'rgb(220,220,220)',
            data: [65, 59, 80, 81, 56, 55, 40]
        },
        {
            label: 'Digital Goods',
            fillColor: 'rgba(0, 123, 255, 0.9)',
            strokeColor: 'rgba(0, 123, 255, 1)',
            pointColor: '#3b8bba',
            pointStrokeColor: 'rgba(0, 123, 255, 1)',
            pointHighlightFill: '#fff',
            pointHighlightStroke: 'rgba(0, 123, 255, 1)',
            data: [28, 48, 40, 19, 86, 27, 90]
        }
    ]
}

var salesChartOptions = {
    //Boolean - If we should show the scale at all
    showScale: true,
    //Boolean - Whether grid lines are shown across the chart
    scaleShowGridLines: false,
    //String - Colour of the grid lines
    scaleGridLineColor: 'rgba(0,0,0,.05)',
    //Number - Width of the grid lines
    scaleGridLineWidth: 1,
    //Boolean - Whether to show horizontal lines (except X axis)
    scaleShowHorizontalLines: true,
    //Boolean - Whether to show vertical lines (except Y axis)
    scaleShowVerticalLines: true,
    //Boolean - Whether the line is curved between points
    bezierCurve: true,
    //Number - Tension of the bezier curve between points
    bezierCurveTension: 0.3,
    //Boolean - Whether to show a dot for each point
    pointDot: false,
    //Number - Radius of each point dot in pixels
    pointDotRadius: 4,
    //Number - Pixel width of point dot stroke
    pointDotStrokeWidth: 1,
    //Number - amount extra to add to the radius to cater for hit detection outside the drawn point
    pointHitDetectionRadius: 20,
    //Boolean - Whether to show a stroke for datasets
    datasetStroke: true,
    //Number - Pixel width of dataset stroke
    datasetStrokeWidth: 2,
    //Boolean - Whether to fill the dataset with a color
    datasetFill: true,
    //String - A legend template
    legendTemplate: '<ul class="<%=name.toLowerCase()%>-legend"><% for (var i=0; i<datasets.length; i++){%><li><span style="background-color:<%=datasets[i].lineColor%>"></span><%=datasets[i].label%></li><%}%></ul>',
    //Boolean - whether to maintain the starting aspect ratio or not when responsive, if set to false, will take up entire container
    maintainAspectRatio: false,
    //Boolean - whether to make the chart responsive to window resizing
    responsive: true
}

//Create the line chart
var salesChart = new Chart($('#salesChart'), {
    type: "line",
    data: salesChartData,
    options: salesChartOptions,
})

//---------------------------
//- END MONTHLY SALES CHART -
//---------------------------

//-------------
//- PIE CHART -
//-------------

var PieData = {
    labels: ['Chrome', 'IE', 'FireFox', 'Safari', 'Opera', 'Navigator'],
    datasets: [{
        data: [700, 500, 400, 600, 300, 100],
        backgroundColor: [
            'rgba(255, 99, 132, 0.2)',
            'rgba(54, 162, 235, 0.2)',
            'rgba(255, 206, 86, 0.2)',
            'rgba(75, 192, 192, 0.2)',
            'rgba(153, 102, 255, 0.2)',
            'rgba(255, 159, 64, 0.2)'
        ]
    }]
}

// Create pie or douhnut chart
// You can switch between pie and douhnut using the method below.
var pieChart = new Chart($('#pieChart'), {
    type: "doughnut",
    data: PieData,
})
// //-----------------
// //- END PIE CHART -
// //-----------------


//-----------------
//- SPARKLINE BAR -
//-----------------
$('.sparkbar').each(function () {
    var $this = $(this)
    $this.sparkline('html', {
        type: 'bar',
        height: $this.data('height') ? $this.data('height') : '30',
        barColor: $this.data('color')
    })
})

//-----------------
//- SPARKLINE PIE -
//-----------------
$('.sparkpie').each(function () {
    var $this = $(this)
    $this.sparkline('html', {
        type: 'pie',
        height: $this.data('height') ? $this.data('height') : '90',
        sliceColors: $this.data('color')
    })
})

//------------------
//- SPARKLINE LINE -
//------------------
$('.sparkline').each(function () {
    var $this = $(this)
    $this.sparkline('html', {
        type: 'line',
        height: $this.data('height') ? $this.data('height') : '90',
        width: '100%',
        lineColor: $this.data('linecolor'),
        fillColor: $this.data('fillcolor'),
        spotColor: $this.data('spotcolor')
    })
})

