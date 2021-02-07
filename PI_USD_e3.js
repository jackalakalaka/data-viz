 
const titleText_PI_USD_e3 = 'Aggregate Personal Income in the USA by year';
const yAxisLabelText_PI_USD_e3 = '';
const PI_USD_e3_notice = 'Money is not adjusted for inflation.'

// Selects first available svg (defd in HTML file)
const svg_PI_USD_e3 = d3.select('#svg_PI_USD_e3');

// Unary + opr parses str's from html file into num's
const width_PI_USD_e3 = +svg_PI_USD_e3.attr('width');
const height_PI_USD_e3 = +svg_PI_USD_e3.attr('height');


const render_PI_USD_e3 = data => {
/**Render fn that takes in data & makes rect
 * for each row of dic
*/
  //Value accessors:
  
  const yValue_PI_USD_e3 = d => d.personal_income;
  //Fn takes input d, a row, and returns wkNum
  const xValue_PI_USD_e3 = d => d.year;
  //Margin defn's
  const margin_PI_USD_e3 = { top: 70, right: 40, bottom: 100, left: 105 };
  const innerWidth_PI_USD_e3 = width - margin_PI_USD_e3.left - margin_PI_USD_e3.right;
  const innerHeight_PI_USD_e3 = height - margin_PI_USD_e3.top - margin_PI_USD_e3.bottom;
  
  const yScale_PI_USD_e3 = d3.scaleLinear() //instance of scaleLinear
  /**max()) accepts 1 row of data dom as input & returns val
   * one wants to compute max over*/
  //Domain is max to zero to flip y-axis
  .domain([0, d3.max(data, yValue_PI_USD_e3)])
    .range([innerHeight_PI_USD_e3, 0]); //innerHeight_PI_USD_e3 refers to non-margin area
  
  //will separate bars & determine ht
  const xScale_PI_USD_e3 = d3.scaleBand()//instance of scaleBand
    //Compute fn over all data's elements
    .domain(data.map(xValue_PI_USD_e3)) //country vals
    .range([0, innerWidth_PI_USD_e3]) //innerWidth_PI_USD_e3 refers to non-margin area
    //padding is proportion of bar width removed towards center
    .padding(0.3);
  
  //Appends group element for axes to original svg
  const g_PI_USD_e3 = svg_PI_USD_e3.append('g')
    .attr('transform', `translate(${margin_PI_USD_e3.left},${margin_PI_USD_e3.top})`);
  
  //Set up y-axis tick labels
  const yAxisTickFormat_PI_USD_e3 = number =>
    //Display tick labels as SI type, w/ 3 sig figs
    d3.format('.2s')(number)
      //Replace suffix
      .replace('G', 'B');
  
  //Create y-axis w/ labels
  const yAxis_PI_USD_e3 = d3.axisLeft(yScale_PI_USD_e3)
    .tickFormat(yAxisTickFormat_PI_USD_e3)
    /* Unary - optr does # and then negation */
    //Length of tick line
    .tickSize(+innerWidth_PI_USD_e3);
  
  //Append group element containing x-axis to g
  const xAxisG_PI_USD_e3 = g_PI_USD_e3.append('g')
    //.call invokes fn w/ this selection. ${} reprs code rather than str lit
    .attr('transform', `translate(-15, ${innerHeight_PI_USD_e3+5})`)
    .call(d3.axisBottom(xScale_PI_USD_e3));

  xAxisG_PI_USD_e3.selectAll('.domain, .tick line').remove();

  xAxisG_PI_USD_e3.selectAll('text')
    .style("text-anchor", "end")
    .attr('transform', 'rotate(-90)');
  
  const yAxisG_PI_USD_e3 = g_PI_USD_e3.append('g').call(yAxis_PI_USD_e3)
      //Translate y-axis's group element
    .attr('transform', `translate(${innerWidth_PI_USD_e3},0)`);

  yAxisG_PI_USD_e3.select('.domain').remove();

  //y-axis label
  //+ Rotate this
  yAxisG_PI_USD_e3.append('text')
    //Bc order ops is R->L, rotation is 1st
    .attr('transform', `translate(${-innerWidth_PI_USD_e3-65}, `+` ${innerHeight_PI_USD_e3/2-35}
      ${innerHeight_PI_USD_e3/2-35}) rotate(-90)`)
    .attr('class', 'axis-label')
    .attr('fill', 'black')
    .text(yAxisLabelText_PI_USD_e3);
  
  
  //Create rectangular bars
  g_PI_USD_e3.selectAll('rect').data(data)
    .enter().append('rect')
      //Maps val to indiv bar length - dc'd
      .attr('height', d => +innerHeight_PI_USD_e3-yScale_PI_USD_e3(yValue_PI_USD_e3(d)))
      /**Each xValue_PI_USD_e3, again, is a country—while xScale_PI_USD_e3 maps country
       * labels to area*/
      /*Sets bar width based on padding defined earlier - dc'd*/
      //Bandwidth: computed w of a single bar
      .attr('width', xScale_PI_USD_e3.bandwidth())
      //x coord for country - dc'd
      .attr('x', d => xScale_PI_USD_e3(xValue_PI_USD_e3(d)))
      //y coord for population, adjusting based on origin loc
      //*?
      .attr('y', d => yScale_PI_USD_e3(yValue_PI_USD_e3(d)));
      
  
  //Adds title
  g_PI_USD_e3.append('text')
      .attr('class', 'title')
      .attr('x', 115)
      .attr('y', -30)
      .text(titleText_PI_USD_e3);

  /*//Add inflation notice
  g_PI_USD_e3.append('text')
      .attr('class', 'title')
      .attr('x', 15)
      .attr('y', 130)
      .text(PI_USD_e3_notice);*/    
};



d3.csv('/PI_USD_e3.csv').then(data => { //Callback fn w/ data as arg
/**Fn loads data and makes XML-HTTP req, loads string of
 * data, and parses str into array of obj's—keys
 * represent columns (country, pop) and values represent
 * vals
*/
  data.forEach(d => { // Parse str's to int's for each row of data, d
    console.log('Test')
    d.personal_income = +d.personal_income;
    d.year = +d.year;
    console.log(d.personal_income, ' ', d.year,'\n')
  });
  
  //Renders one row after another from data.csv
  render_PI_USD_e3(data);
});