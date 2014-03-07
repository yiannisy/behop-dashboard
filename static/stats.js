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
    var names = ['Pkts-DL','Pkts-UL'];
    var colors = Highcharts.getOptions().colors;    
    var _date = new Date();
    for (var i = 0; i < activity_data_s5.length; i++){
	_date = new Date(activity_data_s5[i].tstamp);
	dl_data.push([_date.getTime(),activity_data_s5[i].packets_dl/Math.pow(2,10)]);
	upl_data.push([_date.getTime(),activity_data_s5[i].packets_upl/Math.pow(2,10)])
    }
    var activity = [];
    dl_data.sort(function(a,b){
	return a[0] - b[0]});
    upl_data.sort(function(a,b){
	return a[0] - b[0]});

    activity[0] = { name:'Packets DL - BeHop', step:true, data : dl_data };
    activity[1] = { name:'Packets UL - BeHop', step:true, data : upl_data };

    var dl_data = [];
    var upl_data = [];
    for (var i = 0; i < activity_data_s4.length; i++){
	_date = new Date(activity_data_s4[i].tstamp);
	dl_data.push([_date.getTime(),activity_data_s4[i].packets_dl/Math.pow(2,10)]);
	upl_data.push([_date.getTime(),activity_data_s4[i].packets_upl/Math.pow(2,10)])
    }
    dl_data.sort(function(a,b){
	return a[0] - b[0]});
    upl_data.sort(function(a,b){
	return a[0] - b[0]});

    activity[2] = { name:'Packets DL - LWAPP', step:true, data : dl_data };
    activity[3] = { name:'Packets UL - LWAPP', step:true, data : upl_data };




    var myevent_data = [];
    var idx = 1;
    var event_names = Object.keys(event_data).sort();
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
    }
    

    $('#activity').highcharts({
	chart: {
	    zoomType : 'x',
	    spacingRight : 20,
	    type : 'scatter',
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
                text: 'Packets Per Hour(PPH)'
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
