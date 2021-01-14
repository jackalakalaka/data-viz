 
  const titleText = 'Daily COVID-19 deaths and cases';
  const xAxisLabelText = 'Population';
  
  const svg = d3.select('svg');
  
  //unary + opr parses str's into num's
  const width = +svg.attr('width');
  const height = +svg.attr('height');
  
  
  /**Defs render fn that takes in data & makes rect
   * for each row of dic
  */
  const render = data => {
    //Value accessors:
    const xValue = d => d['population'];
    //Fn takes input d, a row, and returns a country
    const yValue = d => d.country;
    //Margin defn's
    const margin = { top: 50, right: 40, bottom: 77, left: 105 };
    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;
    
    const xScale = d3.scaleLinear() //instance of scaleLinear
    /**max() accepts 1 row of data dom as input & returns val
     * one wants to compute max over - ?*/
    .domain([0, d3.max(data, xValue)])
      .range([0, innerWidth]); //innerWidth refers to non-margin area
    
    //will separate bars & determine ht
    const yScale = d3.scaleBand()
        //Compute fn over all data's elements
      .domain(data.map(yValue)) //country vals
      .range([0, innerHeight]) //innerHeight refers to non-margin area
      //padding is proportion of width removed towards center
      .padding(0.34);
    
    //Appends group element to original svg
    const g = svg.append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);
    
    const xAxisTickFormat = number =>
      d3.format('.3s')(number)
        .replace('G', 'B');
    
    const xAxis = d3.axisBottom(xScale)
      .tickFormat(xAxisTickFormat)
      .tickSize(-innerHeight);
    
    //Append group element containing y-axis to g
    g.append('g')
        //.call invokes fn w/ this selection
      .call(d3.axisLeft(yScale))
      
      .selectAll('.domain, .tick line')
        .remove();
    
    const xAxisG = g.append('g').call(xAxis)
        //Translate x-axis's group element
      .attr('transform', `translate(0,${innerHeight})`);
    
    xAxisG.select('.domain').remove();
    
    //Axis label
    xAxisG.append('text')
        .attr('class', 'axis-label')
        .attr('y', 35)
        .attr('x', innerWidth / 2)
        .attr('fill', 'black')
        .text(xAxisLabelText);
    
        
    //Create rectangular bars
    g.selectAll('rect').data(data)
      .enter().append('rect')
        //Maps val to indiv bar length
        .attr('width', d => xScale(xValue(d)))
        /*Sets bar width based on padding defined earlier*/
        //Bandwidth: computed w of a single bar
        .attr('height', yScale.bandwidth())
        //y coord for country
        .attr('y', d => yScale(yValue(d)));
    
    //Adds title
    g.append('text')
        .attr('class', 'title')
        .attr('y', -10)
        .text(titleText);
  };
  

  /**Fn loads data and makes XML-HTTP req, loads string of
   * data, and parses str into array of obj's—keys
   * represent columns (country, pop) and values represent
   * vals
  */
  d3.csv('static/data.csv').then(data => { //Callback w/ data as arg
    data.forEach(d => { //fn accepts d / 1 row of dic\
        //unary + opr parses str's into num's
      d.population = +d.population * 1000;
    });
    render(data);
  });