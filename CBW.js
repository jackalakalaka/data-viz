 
const titleText2 = 'Cases per week';
const yAxisLabelText2 = 'COVID-19 cases';

//Selects first available svg (defd in HTML file)
const svg2 = d3.select('#svg2');

//unary + opr parses str's from html file into num's
const width2 = +svg2.attr('width');
const height2 = +svg2.attr('height');

/**Defs render fn that takes in data & makes rect
 * for each row of dic
*/
 //render is fn name & data is param
 //? - d
const render2 = data => {
  //Value accessors:
  const yValue2 = d => d.covid_19_deaths;
  //Fn takes input d, a row, and returns a country
  const xValue2 = d => d.weekNum;
  //Margin defn's
  const margin2 = { top: 70, right: 40, bottom: 100, left: 105 };
  const innerWidth2 = width2 - margin2.left - margin2.right;
  const innerHeight2 = height2 - margin2.top - margin2.bottom;
  
  const yScale2 = d3.scaleLinear() //instance of scaleLinear
  /**max()) accepts 1 row of data dom as input & returns val
   * one wants to compute max over*/
  //Domain is max to zero to flip y-axis
  .domain([0, d3.max(data, yValue2)])
    .range([innerHeight2, 0]); //innerHeight refers to non-margin area
  
  //will separate bars & determine ht
  const xScale2 = d3.scaleBand()//instance of scaleBand
    //Compute fn over all data's elements
    .domain(data.map(xValue2)) //country vals
    .range([0, innerWidth2]) //innerWidth refers to non-margin area
    //padding is proportion of bar width removed towards center
    .padding(0.3);
  
  //Appends group element for axes to original svg
  const g2 = svg2.append('g')
    .attr('transform', `translate(${margin2.left},${margin2.top})`);
  
  //Set up y-axis tick labels
  const yAxisTickFormat2 = number =>
    //Display tick labels as SI type, w/ 3 sig figs
    d3.format('.2s')(number)
      //Replace suffix
      .replace('G', 'B');
  
  //Create y-axis w/ labels
  const yAxis2 = d3.axisLeft(yScale2)
    .tickFormat(yAxisTickFormat2)
    /* Unary - optr does # and then negation */
    //Length of tick line
    .tickSize(+innerWidth2);
  
  //Append group element containing x-axis to g
  const xAxisG2 = g2.append('g')
    //.call invokes fn w/ this selection. ${} reprs code rather than str lit
    .attr('transform', `translate(-15, ${innerHeight2+5})`)
    .call(d3.axisBottom(xScale2));

  xAxisG2.selectAll('.domain, .tick line').remove();

  xAxisG2.selectAll('text')
    .style("text-anchor", "end")
    .attr('transform', 'rotate(-90)');
  
  const yAxisG2 = g2.append('g').call(yAxis2)
      //Translate y-axis's group element
    .attr('transform', `translate(${innerWidth2},0)`);

  yAxisG2.select('.domain').remove();

  //y-axis label
  //+ Rotate this
  yAxisG2.append('text')
    //Bc order ops is R->L, rotation is 1st
    .attr('transform', `translate(${innerWidth2-65}, `+` ${innerHeight2/2-35}
      ${innerHeight2/2-35}) rotate(-90)`)
    .attr('class', 'axis-label')
    .attr('fill', 'black')
    .text(yAxisLabelText2);
  

  //Create rectangular bars
  g2.selectAll('rect').data(data)
    .enter().append('rect')
      //Maps val to indiv bar length - dc'd
      .attr('height', d => innerHeight2-yScale2(yValue2(d)))
      /**Each xValue, again, is a country—while xScale maps country
       * labels to area*/
      /*Sets bar width based on padding defined earlier - dc'd*/
      //Bandwidth: computed w of a single bar
      .attr('width', xScale2.bandwidth())
      //x coord for country - dc'd
      .attr('x', d => xScale2(xValue2(d)))
      //y coord for population, adjusting based on origin loc
      //*?
      .attr('y', d => yScale2(yValue2(d)));
      
  
  //Adds title
  g2.append('text')
      .attr('class', 'title')
      .attr('x', 115)
      .attr('y', -30)
      .text(titleText2);
};



/**Fn loads data and makes XML-HTTP req, loads string of
 * data, and parses str into array of obj's—keys
 * represent columns (country, pop) and values represent
 * vals
*/
d3.csv('/COVID19DeathsByWeek_Age.csv').then(data => { //Callback w/ data as arg
  data.forEach(d => { //fn accepts d / 1 row of dic
      //unary + opr parses str's into num's
    d.total_deaths = +d.total_deaths;
    d.covid_19_deaths = +d.covid_19_deaths;
    
  });
  //Add numbered week column to array dics
  //dataRow = {};
  var wkNum = 1;
  for (var i=0; i < data.length; i++) {
    data[i]['weekNum'] = wkNum;
    if (i%11==0){
      wkNum++;
    }
  }
  
  //Renders one row after another from data.csv
  render2(data);
});