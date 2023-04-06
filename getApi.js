
//il faut installer puppeteer et html-table-to-json avec npm install
const puppeteer = require('puppeteer');
const HtmlTableToJson = require('html-table-to-json');


async function getInfo(teacher) {

    const browser = await puppeteer.launch({
        
        headless: true,
        // This setting allows us to scrape non-https websites easier
        ignoreHTTPSErrors: true,
        defaultViewport: null,
    });
    // Create a new page
    const page = await browser.newPage();
    await page.goto('http://sco.polytech.unice.fr/1/invite?fd=1', {waitUntil: 'domcontentloaded'});

    //click on the menu(ENSEIGNANT)
    
    let menu=await page.waitForXPath(`//*[@id="GInterface.Instances[0]"]/div/div[3]`)
    await menu?.$eval('ul > li', el => el.click());
    


    //Change type grid to list view
    let dropmenu=await page.waitForXPath(`//*[@id="GInterface.Instances[0]_secondMenu"]/div[1]/ul/li[1]`)
    await dropmenu?.$eval('ul', el => el.children[1].click());

    //Select search bar
    await page.waitForSelector('input[type=text]');

    //Change value of search bar
    await page.$eval('input[type=text]', (el,teacher) => { el.value = teacher; },teacher);
    //Press enter
    await (await page.$('input[type="text"]'))?.press('Enter');
    await page.evaluate(async() => {
        await new Promise(function(resolve) { 
               setTimeout(resolve,1500)
        });
    });
    
    //Get table with info
    let HtmlTable=await page.waitForXPath(`//*[@id="GInterface.Instances[1].Instances[7]"]/div`);
    //get all emelent of table
    const table = await HtmlTable?.$eval('table', el => el.innerText);
    let res = parseTable(table,teacher)
    
    //close browser
    await browser.close();
    return res}


//function that parse the table and return a json
function parseTable(table,teacher){
   const days=["lundi","mardi","mercredi","jeudi","vendredi","samedi","dimanche"]
   var effectiveDays=[]
   var separateDays=[]
   var res = []

   //Loop to determine the effective days (= the days on which there are classes)
   for ( let day of days){
        let index = table?.indexOf(day)
        if (index != -1){
            effectiveDays.push(index)
        }
   }

    //Loop to collect classes of each effective day
   for (let i = 0; i<effectiveDays.length; i++){
       separateDays.push(table?.slice(effectiveDays[i],effectiveDays[i+1]))
   }
   

   //Once we have all the classes of each day, we can parse them
   //We can manipulate the array like this : separateClasses[0][1] for the first day and the first class
   const separateClasses = (separateDays.map(el => el.split("\t\n")));
   
    //Loop to parse each class
    for (let i = 0; i<separateClasses.length; i++){
        for (let j = 1; j<separateClasses[i].length; j++){
            let classInfo = separateClasses[i][j].split("\t")
            const group = classInfo[3].match(/TD [0-9]+/g) || [""]
            let classInfoJson = {
                "day": separateClasses[i][0],
                "time": classInfo[1],
                "name": classInfo[2],
                "type": classInfo[3],
                "room": classInfo[4],
                "teacher": teacher,
                "group": group[0]
            }
            res.push(classInfoJson)
        }
    }
    return res
}

let profs = ["BUFFA Michel", "DONATI Leo", "WINTER Michel"]
let resultat = []
for (let prof of profs){
    resultat.push(getInfo(prof))
}

Promise.all(resultat).then((res) => {
    console.log(res)
})