"use strict";
/* MAP-01 browser acceptance tests: real Leaflet UI with checked-in NASA FIRMS snapshot. */
const assert=require("node:assert/strict");
const fs=require("node:fs");
const puppeteer=require("puppeteer-core");
const src=JSON.parse(fs.readFileSync("data/recente.json","utf8"));
const n20=(src.detections||[]).filter(x=>x.sensor==="NOAA20").length;
const n21=(src.detections||[]).filter(x=>x.sensor==="NOAA21").length;
async function run(){
 const browser=await puppeteer.launch({headless:true,executablePath:process.env.CHROME_BIN,
  args:["--no-sandbox","--disable-dev-shm-usage"]});
 const page=await browser.newPage();
 const errors=[];
 page.on("pageerror",e=>errors.push(e.message));
 page.setDefaultTimeout(20000);
 try{
  await page.setViewport({width:1280,height:900});
  await page.goto("http://127.0.0.1:8123/?lang=en",{waitUntil:"domcontentloaded",timeout:45000});
  await page.waitForFunction(()=>document.querySelectorAll(".map-list-point").length>0,{timeout:30000});
  const displayed=()=>page.$eval("#map-count",e=>e.textContent.trim());
  assert.match(await displayed(),new RegExp("^"+(n20+n21)+" "));
  const mapExists=await page.evaluate(()=>Boolean(document.querySelector("#fire-map.leaflet-container")));
  assert.equal(mapExists,true,"Leaflet map initialized");
  await page.click("#map-point-list .map-list-point");
  let detail=await page.$eval("#map-inspector-details",e=>e.textContent);
  assert.match(detail,/Scientific translator/);assert.match(detail,/Human translator/);
  assert.match(detail,/NOAA-20/);assert.match(detail,/Latitude|Coordinates/);
  assert.match(detail,/Normal \(n\)|High \(h\)/);
  console.log("MAP-01: point selection renders real scientific and human attributes");
  await page.click('[data-map-filter="NOAA21"]');
  assert.match(await displayed(),new RegExp("^"+n21+" "));
  await page.click("#map-point-list .map-list-point");
  detail=await page.$eval("#map-inspector-details",e=>e.textContent);
  assert.match(detail,/NOAA-21/);assert.match(detail,/Scientific translator/);
  await page.click('[data-map-filter="NOAA20"]');assert.match(await displayed(),new RegExp("^"+n20+" "));
  await page.click('[data-map-filter="all"]');assert.match(await displayed(),new RegExp("^"+(n20+n21)+" "));
  console.log("MAP-01: NOAA-20, NOAA-21 and combined filter counts verified");
  await page.click("#map-point-list .map-list-point");
  await page.click('[data-language="pt-BR"]');
  detail=await page.$eval("#map-inspector-details",e=>e.textContent);
  assert.match(detail,/Tradutor científico/);assert.match(detail,/Tradutor humano/);
  assert.match(await page.$eval("#map-section-title",e=>e.textContent),/Explore as detecções/);
  await page.click('[data-language="en"]');
  assert.match(await page.$eval("#map-inspector-details",e=>e.textContent),/Scientific translator/);
  console.log("MAP-01: complete EN/PT-BR toggle with selected point");
  await page.setViewport({width:390,height:844});
  await page.waitForTimeout(300);
  const geo=await page.evaluate(()=>({map:document.querySelector("#fire-map").getBoundingClientRect().width,
   wrap:document.querySelector(".map-explorer").getBoundingClientRect().width,
   list:document.querySelector(".map-point-list").getBoundingClientRect().width,
   h:document.querySelector("#fire-map").getBoundingClientRect().height}));
  assert.ok(geo.wrap<=390&&geo.map>270&&geo.map<=geo.wrap&&geo.h>=300,"mobile map layout");
  await page.click("#map-point-list .map-list-point");
  assert.match(await page.$eval("#map-inspector-details",e=>e.textContent),/Scientific translator/);
  console.log("MAP-01: mobile 390x844, list selection and map layout verified");
  assert.deepEqual(errors,[],"no browser uncaught JavaScript errors");
  await page.setRequestInterception(true);
  page.on("request",req=>{
   if(req.url().includes("/data/recente.json"))req.respond({status:200,contentType:"application/json",body:JSON.stringify({status:"unavailable",detections:[],last_success_utc:null})});
   else req.continue();
  });
  await page.reload({waitUntil:"domcontentloaded"});
  await page.waitForFunction(()=>document.querySelector("#map-status").textContent.includes("No available NASA detections"));
  assert.equal(await page.$eval("#map-point-list",e=>e.children.length),0);
  assert.equal(await page.$eval("#map-no-data",e=>e.hidden),false);
  console.log("MAP-01: unavailable NASA feed shows zero plotted points and explicit warning");
 }finally{await browser.close();}
}
run().catch(e=>{console.error(e);process.exitCode=1;});
