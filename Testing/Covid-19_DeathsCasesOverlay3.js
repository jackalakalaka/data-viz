const data = [
    { name: 'John', score: 80 },
    { name: 'Simon', score: 76 },
    { name: 'Samantha', score: 90 },
    { name: 'Patrick', score: 82 },
    { name: 'Mary', score: 90 },
    { name: 'Christina', score: 75 },
    { name: 'Michael', score: 86 },
  ];
  
  //Total svg dims w/ margin
  const width = 900;
  const height = 450;
  const margin = { top: 50, bottom: 50, left: 50, right: 50 };
  
  //Selects div from b4, w/ # selector for id
  const svg = d3.select('#d3-container')
    .append('svg')
    .attr('width', width - margin.left - margin.right)
    .attr('height', height - margin.top - margin.bottom)
    /**viewBox defs dims of svg viewPort, which makes a
     * defd prt of the svg visible*/
    .attr("viewBox", [0, 0, width, height]);
  
  const xScale = d3.scaleBand()
    //Create scale from 0 through ~len of data dim
    .domain(d3.range(data.length)) //length dim of data array
    .range([margin.left, width - margin.right])
    .padding(0.1);
  
  const yScale = d3.scaleLinear()
    .domain([0, 100])
    .range([height - margin.bottom, margin.top]);
  
  svg
    .append("g")
    .attr("fill", 'royalblue')//Color
    .selectAll("rect")
    //Pass in data & sort it in desc order
    //* remove
    .data(data.sort((a, b) => d3.descending(a.score, b.score)))
    .join("rect")
      //Scaled x-val/loc of partlr indx
      //? - how does d come into play
      .attr("x", (d, i) => xScale(i))//d-data, i-index
      //Scaled y loc
      //? - shouldn't all be at x-axis height>
      .attr("y", d => yScale(d.score))
      .attr('title', (d) => d.score)
      //Def class to be selected in html file for interactivity
      .attr("class", "rect")
      //Pass 0 into yScale & implement bar height
      .attr("height", d => yScale(0) - yScale(d.score))
      //Calcs correct width based on padding arg
      .attr("width", xScale.bandwidth());
  
  function yAxis(g) {
    g.attr("transform", `translate(${margin.left}, 0)`)
      .call(d3.axisLeft(yScale).ticks(null, data.format))//? - .format
      .attr("font-size", '20px')
  }
  
  function xAxis(g) {
    //Bring from top to bottom
    g.attr("transform", `translate(0,${height - margin.bottom})`)
      //Pass in index & disp element's name
      .call(d3.axisBottom(xScale).tickFormat(i => data[i].name))//Formatted as ticks
      .attr("font-size", '20px')
  }
  
  svg.append("g").call(xAxis);
  svg.append("g").call(yAxis);
  svg.node();