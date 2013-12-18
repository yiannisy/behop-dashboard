var margin = {top: 20, right: 20, bottom: 100, left: 50},
    margin2 = {top: 430, right: 20, bottom: 20, left: 50},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom,
    height2 = 500 - margin2.top - margin2.bottom;

var parseDate = d3.time.format.utc("%Y-%m-%d %H:%M:%S+00:00").parse;

var x = d3.scale.linear().range([0, width]);

var y = d3.scale.linear().range([height, 0]);

var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");

var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left");

var line = d3.svg.line()
    .x(function(d) { return x(d.rtt); })
    .y(function(d,i) { return y(i/data.length); });

var svg = d3.select("#rtt").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom);

svg.append("defs").append("clipPath")
    .attr("id", "clip")
  .append("rect")
    .attr("width", width)
    .attr("height", height);

var focus = svg.append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var context = svg.append("g")
    .attr("transform", "translate(" + margin2.left + "," + margin2.top + ")");

var data = rtt_data;
data.sort(function(a,b){
    return a.rtt - b.rtt});

x.domain([0,100]); //d3.extent(data, function(d) { return +d.rtt; }));
y.domain([0,1]);

focus.append("path")
    .datum(data)
    .attr("class", "line")
    .attr("d", line);

focus.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + height + ")")
    .call(xAxis);

focus.append("g")
    .attr("class", "y axis")
    .call(yAxis)
    .append("text")
//.attr("transform", "rotate(-90)")
    .attr("y", -12)
    .attr("dy", ".71em")
    .style("text-anchor", "end")
    .text("CDF");



