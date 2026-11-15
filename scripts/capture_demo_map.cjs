"use strict";
const puppeteer=require("puppeteer-core"),fs=require("node:fs");
(async()=>{
 const browser=await puppeteer.launch({headless:true,executablePath:process.env.CHROME_BIN,
  args:["--no-sandbox","--disable-dev-shm-usage"]});
 try{
  const page=await browser.newPage();
  await page.setViewport({width:1360,height:900,deviceScaleFactor:1.4});
  await page.goto("http://127.0.0.1:8124/?lang=en",{waitUntil:"domcontentloaded",timeout:45000});
  await page.waitForFunction(()=>document.querySelectorAll(".map-list-point").length>0 &&
    !document.querySelector("#map-show-case").disabled,{timeout:35000});
  await new Promise(resolve=>setTimeout(resolve,3000));
  await page.$eval("#map-explorer",e=>e.scrollIntoView({block:"start"}));
  await (await page.$("#map-explorer")).screenshot({path:"/tmp/firelens_recent.png"});
  await page.click("#map-show-case");
  await page.waitForFunction(()=>document.querySelectorAll(".map-pixel.case-viirs").length===2);
  await page.click(".map-measurements summary");
  await (await page.$("#map-explorer")).screenshot({path:"/tmp/firelens_eagle.png"});
  await page.click('[data-view="calendario"]');
  await page.waitForSelector("#calendar .heat-cell:not([disabled])");
  await page.$eval("#calendario",e=>e.scrollIntoView({block:"start"}));
  await (await page.$("#calendario")).screenshot({path:"/tmp/firelens_history.png"});
  console.log("REAL_APP_SCREENSHOTS",JSON.stringify(["/tmp/firelens_recent.png","/tmp/firelens_eagle.png","/tmp/firelens_history.png"].map(p=>({path:p,bytes:fs.statSync(p).size}))));
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1});
