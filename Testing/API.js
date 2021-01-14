/**Returns promise, which deals w/ async ctrl flow
 * which is not necessarily immediate. Promise either
 * succeeds or resolves*/
const csvURL = 'https://data.cdc.gov/resource/vsak-wrfu.csv';

/**Def fn that takes resp at input. This is a callback fn,
 * bc it is called back when something is rdy.*/

//const promise = fetch(url);
//promise.then(response => {
//    /**.text reads resp stream to completion & rets txt.
//     * It also rets a promise, so need callback fn*/
//    response.text().then(text => {
//        console.log(response);
//    });
//});

/**Instead of forming an indentation pyramid of doom, use
 * async or await
 */
const fetchText = async (url) => {
    const response = await fetch(url);
    return await response.text();
    //console.log(text);
}

fetchText(csvURL).then(text =>{
    //console.log(text);
    (async () => {
    
        // Modify the cars
        console.log(text[20]);
    
        // Saved the cars
        //const carsInCsv = new Parser({ fields: ["Year", "Make", "Model", "Length"] }).parse(cars);
        //fs.writeFileSync("cars.csv", carsInCsv);
    
    })();
})

/**When make net req, comes back in a stream rather than
 * all at once*/
