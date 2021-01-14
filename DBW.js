 
const titleText = 'Deaths per week in the USA';
const yAxisLabelText = '';

// Selects first available svg (defd in HTML file)
const svg = d3.select('#svg1');

// Unary + opr parses str's from html file into num's
const width = +svg.attr('width');
const height = +svg.attr('height');


const render = data => {
/**Render fn that takes in data & makes rect
 * for each row of dic
*/
  //Value accessors:
  
  const yValue = d => d.covid_19_deaths;
  //Fn takes input d, a row, and returns wkNum
  const xValue = d => d.wkNum;
  //Margin defn's
  const margin = { top: 70, right: 40, bottom: 100, left: 105 };
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;
  
  const yScale = d3.scaleLinear() //instance of scaleLinear
  /**max()) accepts 1 row of data dom as input & returns val
   * one wants to compute max over*/
  //Domain is max to zero to flip y-axis
  .domain([0, d3.max(data, yValue)])
    .range([innerHeight, 0]); //innerHeight refers to non-margin area
  
  //will separate bars & determine ht
  const xScale = d3.scaleBand()//instance of scaleBand
    //Compute fn over all data's elements
    .domain(data.map(xValue)) //country vals
    .range([0, innerWidth]) //innerWidth refers to non-margin area
    //padding is proportion of bar width removed towards center
    .padding(0.3);
  
  //Appends group element for axes to original svg
  const g = svg.append('g')
    .attr('transform', `translate(${margin.left},${margin.top})`);
  
  //Set up y-axis tick labels
  const yAxisTickFormat = number =>
    //Display tick labels as SI type, w/ 3 sig figs
    d3.format('.2s')(number)
      //Replace suffix
      .replace('G', 'B');
  
  //Create y-axis w/ labels
  const yAxis = d3.axisLeft(yScale)
    .tickFormat(yAxisTickFormat)
    /* Unary - optr does # and then negation */
    //Length of tick line
    .tickSize(+innerWidth);
  
  //Append group element containing x-axis to g
  const xAxisG = g.append('g')
    //.call invokes fn w/ this selection. ${} reprs code rather than str lit
    .attr('transform', `translate(-15, ${innerHeight+5})`)
    .call(d3.axisBottom(xScale));

  xAxisG.selectAll('.domain, .tick line').remove();

  xAxisG.selectAll('text')
    .style("text-anchor", "end")
    .attr('transform', 'rotate(-90)');
  
  const yAxisG = g.append('g').call(yAxis)
      //Translate y-axis's group element
    .attr('transform', `translate(${innerWidth},0)`);

  yAxisG.select('.domain').remove();

  //y-axis label
  //+ Rotate this
  yAxisG.append('text')
    //Bc order ops is R->L, rotation is 1st
    .attr('transform', `translate(${-innerWidth-65}, `+` ${innerHeight/2-35}
      ${innerHeight/2-35}) rotate(-90)`)
    .attr('class', 'axis-label')
    .attr('fill', 'black')
    .text(yAxisLabelText);
  
  
  //Create rectangular bars
  g.selectAll('rect').data(data)
    .enter().append('rect')
      //Maps val to indiv bar length - dc'd
      .attr('height', d => +innerHeight-yScale(yValue(d)))
      /**Each xValue, again, is a country—while xScale maps country
       * labels to area*/
      /*Sets bar width based on padding defined earlier - dc'd*/
      //Bandwidth: computed w of a single bar
      .attr('width', xScale.bandwidth())
      //x coord for country - dc'd
      .attr('x', d => xScale(xValue(d)))
      //y coord for population, adjusting based on origin loc
      //*?
      .attr('y', d => yScale(yValue(d)));
      
  
  //Adds title
  g.append('text')
      .attr('class', 'title')
      .attr('x', 115)
      .attr('y', -30)
      .text(titleText);
};



d3.csv('/DBW.csv').then(data => { //Callback fn w/ data as arg
/**Fn loads data and makes XML-HTTP req, loads string of
 * data, and parses str into array of obj's—keys
 * represent columns (country, pop) and values represent
 * vals
*/
  data.forEach(d => { // Parse str's to int's for each row of data, d
    d.total_deaths = +d.total_deaths;
    d.covid_19_deaths = +d.covid_19_deaths;
  });
  
  //Renders one row after another from data.csv
  console.log(data.length);
  render(data);
});