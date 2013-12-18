var margin = {top: 20, right: 20, bottom: 100, left: 50},
    margin2 = {top: 430, right: 20, bottom: 20, left: 50},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom,
    height2 = 500 - margin2.top - margin2.bottom;

var parseDate = d3.time.format.utc("%Y-%m-%d %H:%M:%S").parse;

var x = d3.time.scale().range([0, width]),
    x2 = d3.time.scale().range([0, width]);

var y = d3.scale.linear().range([height, 0]),
    y2 = d3.scale.linear().range([height2, 0]);

var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");

var xAxis2 = d3.svg.axis()
    .scale(x2)
    .orient("bottom");

var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left");

var brush = d3.svg.brush()
    .x(x2)
    .on("brush", brushed);

var line = d3.svg.line()
    .x(function(d) {  return x(parseDate(d.tstamp.substring(0,19))); })
    .y(function(d) { return y(d.rtt); });

var line2 = d3.svg.line()
    .x(function(d) { return x2(parseDate(d.tstamp.substring(0,19))); })
    .y(function(d) { return y2(d.rtt); });

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

data = rtt_data;
console.log(data);

x.domain(d3.extent(data, function(d) { return +parseDate(d.tstamp.substring(0,19)); }));
y.domain(d3.extent(data, function(d) { return +d.rtt; }));
x2.domain(x.domain());
y2.domain(y.domain());

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
    .text("RTT");

context.append("path")
    .datum(data)
    .attr("class", "line")
    .attr("d", line2);

context.append("g")
    .attr("class", "x axis")
    .attr("transfrom", "translate(0," + height2 + ")")
    .call(xAxis2);

context.append("g")
    .attr("class", "x brush")
    .call(brush)
    .selectAll("rect")
    .attr("y", -6)
    .attr("height", height2 + 7);

function brushed() {
  x.domain(brush.empty() ? x2.domain() : brush.extent());
  focus.select("path").attr("d", line);
  focus.select(".x.axis").call(xAxis);
}


