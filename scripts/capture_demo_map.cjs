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
  // Give OpenStreetMap tiles time to settle after the archived case map zoom.
  await new Promise(resolve=>setTimeout(resolve,3000));
  // Preserve the compact inspector; expanded measurements would make this image
  // disproportionately tall and unreadable within a single demonstration slide.
  await (await page.$("#map-explorer")).screenshot({path:"/tmp/firelens_eagle.png"});
  await page.click('[data-view="calendario"]');
  // Capture HIST-02 as the public site's DEFAULT, not the hidden A/B experiment.
  await page.waitForFunction(()=>
    document.querySelector('[data-history-view="state"]')?.getAttribute("aria-pressed")==="true" &&
    document.querySelectorAll("#state-calendar .state-heat-cell:not(:disabled)").length===40 &&
    document.querySelectorAll("#state-calendar .state-heat-cell:disabled").length===8,
    {timeout:30000});
  await page.click("#state-calendar .state-year-row:last-child .state-heat-cell:nth-child(10)");
  await page.waitForFunction(()=>
    document.querySelector("#state-calendar-detail")?.textContent.includes("3,518") &&
    document.querySelector("#state-calendar-detail")?.textContent.includes("NRT"));
  const hist=await page.evaluate(()=>({
    primary:document.querySelector('[data-history-view="state"]').getAttribute("aria-pressed"),
    aqua:document.querySelector('[data-state-sensor="Aqua"]').getAttribute("aria-pressed"),
    pilotHidden:document.querySelector("#pilot-history").hidden,
    note:document.querySelector("#state-calendar-detail").textContent,
    partial:document.querySelector(".year-partial").textContent,
    months:document.querySelectorAll("#state-calendar .state-heat-cell:not(:disabled)").length
  }));
  if(hist.primary!=="true"||hist.aqua!=="true"||!hist.pilotHidden||!hist.partial.includes("PARTIAL")||hist.months!==40)
    throw Error("HIST-02 screenshot source not validated: "+JSON.stringify(hist));
  await page.$eval("#state-history .wide-panel",e=>e.scrollIntoView({block:"center"}));
  await (await page.$("#state-history .wide-panel")).screenshot({path:"/tmp/firelens_history.png"});
  console.log("DEMO02_HIST_SOURCE",JSON.stringify(hist));
  console.log("REAL_APP_SCREENSHOTS",JSON.stringify(["/tmp/firelens_recent.png","/tmp/firelens_eagle.png","/tmp/firelens_history.png"].map(p=>({path:p,bytes:fs.statSync(p).size}))));
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1});
