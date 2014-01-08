$(function () {
    netflix_data.sort(function(a,b){
	return a.rate -b.rate});
    youtube_data.sort(function(a,b){
	return a.rate - b.rate});
    rtt_data.sort(function(a,b){
	return a.rtt - b.rtt});

    var netflix_rates = [];
    for (var i = 0; i < netflix_data.length; i++){
	netflix_rates.push([netflix_data[i].rate,i/netflix_data.length]);
    }

    var youtube_rates = [];
    for (var i = 0; i < youtube_data.length; i++){
	youtube_rates.push([youtube_data[i].rate,i/youtube_data.length]);
    }

    var rtt = [];
    for (var i = 0; i < rtt_data.length; i++){
	if (rtt_data[i].rtt == 0){
	    rtt_data[i].rtt = 0.1;
	}
	rtt.push([rtt_data[i].rtt, i/rtt_data.length]);
    }

    $('#netflix').highcharts({
	chart: {
	    zoomType : 'x',
	    spacingRight : 20
	},
        title: {
            text: 'Netflix Video Rate for Studio 5',
            x: -20 //center
        },
	xAxis: {
            title: {
                text: 'Video Rate'
            },
            tickInterval: 500,
	    min : 200,
	    max : 6000,

        },
        yAxis: {
            title: {
                text: 'CDF'
            },
	    min : 0,
	    max : 1.1
        },
        tooltip: {
            valueSuffix: '%'
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle',
            borderWidth: 0
        },
        series: [{
            name: 'Netflix',
            data: netflix_rates
        }]
    });

    $('#youtube').highcharts({
        title: {
            text: 'Youtube Video Rate for Studio 5',
            x: -20 //center
        },
	xAxis: {
            title: {
                text: 'Video Rate'
            },
	    min : 100,
	    max : 6000,
            tickInterval: 500
        },
        yAxis: {
            title: {
                text: 'CDF'
            },
	    min : 0,
	    max : 1.1,
        },
        tooltip: {
            valueSuffix: '%'
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle',
            borderWidth: 0
        },
        series: [{
            name: 'Youtube',
            data: youtube_rates
        }]
    });

    $('#rtt').highcharts({
	chart: {
	    zoomType : 'x',
	    spacingRight : 20
	},
        title: {
            text: 'Packet Delivery Time for Studio 5',
            x: -20 //center
        },
	xAxis: {
            title: {
                text: 'PDT'
            },
            tickInterval: 50
        },
        yAxis: {
            title: {
                text: 'CDF'
            },
	    min : 0,
	    max : 1.1
        },
        tooltip: {
            valueSuffix: '%'
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle',
            borderWidth: 0
        },
        series: [{
            name: 'RTT',
            data: rtt
        }]
    });


});
