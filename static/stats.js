$(function () {
    Highcharts.setOptions({
        global: {
            useUTC: false
        }
    });

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

    var dl_data = [];
    var upl_data = [];
    var names = ['Bytes DL','Bytes UPL'];
    var colors = Highcharts.getOptions().colors;    
    var _date = new Date();
    for (var i = 0; i < activity_data.length; i++){
	_date = new Date(activity_data[i].tstamp);
	dl_data.push([_date.getTime(),activity_data[i].bytes_dl/Math.pow(2,20)]);
	upl_data.push([_date.getTime(),activity_data[i].bytes_upl/Math.pow(2,20)])
    }
    var activity = [];
    dl_data.sort(function(a,b){
	return a[0] - b[0]});
    upl_data.sort(function(a,b){
	return a[0] - b[0]});

    activity[0] = { name:'Bytes DL', step:true, data : dl_data };
    activity[1] = { name:'Bytes UPL', step:true, data : upl_data };

    var myevent_data = [];
    var idx = 1;
    var event_names = Object.keys(event_data).sort();
    console.log(event_names);
    for (var j = 0; j < event_names.length; j++){
	var event = event_names[j];
	var data = [];
	for (i = 0; i < event_data[event].length; i++){
	    _date = new Date(event_data[event][i].tstamp);
	    data[i] = [_date.getTime(),idx];
	}
	data.sort(function(a,b){ return a[0]-b[0] });
	myevent_data.push({name:event,data:data})
	idx = idx + 1;
	console.log(data);
    }
    

    $('#activity').highcharts({
	chart: {
	    zoomType : 'x',
	    spacingRight : 20
	},

        title: {
            text: 'Activity',
            x: -20 //center
        },
	xAxis: {
	    maxZoon : 7*24*3600000,
	    type: 'datetime',
            title: {
                text: 'Time'
            },
        },
        yAxis: {
            title: {
                text: 'Traffic (MB)'
            },
        },
	tooltip: {
	    formatter: function() {
		return '<b>' + this.series.name + '</b><br/>' + Highcharts.dateFormat("%A, %b %e, %H:%M:%S",
										      new Date(this.x));},

	},
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle',
            borderWidth: 0
        },
        series: activity
    });

    $('#events').highcharts({
	chart: {
	    zoomType : 'x',
	    spacingRight : 20
	},

        title: {
            text: 'Activity',
            x: -20 //center
        },
	xAxis: {
	    maxZoon : 7*24*3600000,
	    type: 'datetime',
            title: {
                text: 'Time'
            },
        },
        yAxis: {
            title: {
                text: 'Traffic (MB)'
            },
	    type : 'category'
        },
	tooltip: {
	    formatter: function() {
		return '<b>' + this.series.name + '</b><br/>' + Highcharts.dateFormat("%A, %b %e, %H:%M:%S",
										      new Date(this.x));},

	},
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle',
            borderWidth: 0
        },
        series: myevent_data
    });




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
            tickInterval: 50,
	    min: 0,
	    max: 1000
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
