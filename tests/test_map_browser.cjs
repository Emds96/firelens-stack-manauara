"use strict";
/* FIN-01 / UX-03 browser acceptance: actual NASA JSON and archived Eagle case. */
const assert=require("node:assert/strict");
const fs=require("node:fs");
const puppeteer=require("puppeteer-core");
const src=JSON.parse(fs.readFileSync("data/recente.json","utf8"));
const archived=JSON.parse(fs.readFileSync("data/caso_visao_aguia_20261110.json","utf8"));
const n20=(src.detections||[]).filter(x=>x.sensor==="NOAA20").length;
const n21=(src.detections||[]).filter(x=>x.sensor==="NOAA21").length;
async function run(){
 const browser=await puppeteer.launch({headless:true,executablePath:process.env.CHROME_BIN,
  args:["--no-sandbox","--disable-dev-shm-usage"]});
 const page=await browser.newPage();
 const errors=[];
 page.on("pageerror",e=>errors.push(e.message));
 page.setDefaultTimeout(25000);
 try{
  await page.setViewport({width:1280,height:900});
  await page.goto("http://127.0.0.1:8123/?lang=en",{waitUntil:"domcontentloaded",timeout:45000});
  await page.waitForFunction(()=>document.querySelectorAll(".map-list-point").length>0 && !document.querySelector("#map-show-case").disabled,{timeout:35000});
  const displayed=()=>page.$eval("#map-count",e=>e.textContent.trim());
  assert.match(await displayed(),new RegExp("^"+(n20+n21)+" "));
  assert.equal(await page.$eval("#fire-map",e=>e.classList.contains("leaflet-container")),true);
  assert.equal(await page.$eval('[data-view="agora"]',e=>e.getAttribute("aria-selected")),"true");
  assert.equal(await page.$eval("#recent-secondary",e=>e.open),false);
  console.log("FIN-01: map is first, statistics collapsed, true NASA NRT visible");

  await page.click("#map-point-browser summary");
  await page.click("#map-point-list .map-list-point");
  let detail=await page.$eval("#map-inspector-details",e=>e.textContent);
  assert.match(detail,/satellite detected a thermal anomaly/i);
  assert.match(detail,/not confirm an individual fire/i);
  assert.doesNotMatch(detail,/Scientific translator|Human translator/);
  assert.equal(await page.$eval(".map-measurements",e=>e.open),false);
  await page.click(".map-measurements summary");
  detail=await page.$eval("#map-inspector-details",e=>e.textContent);
  assert.match(detail,/Coordinates/);assert.match(detail,/NOAA-20/);
  console.log("FIN-01: selected point has one understandable explanation and expandable measurements");

  await page.click('[data-map-filter="NOAA21"]');
  assert.match(await displayed(),new RegExp("^"+n21+" "));
  await page.click("#map-point-list .map-list-point");
  detail=await page.$eval("#map-inspector-details",e=>e.textContent);
  assert.match(detail,/NOAA-21/);
  await page.click('[data-map-filter="NOAA20"]');assert.match(await displayed(),new RegExp("^"+n20+" "));
  await page.click('[data-map-filter="all"]');assert.match(await displayed(),new RegExp("^"+(n20+n21)+" "));
  console.log("MAP-01 retained: satellite filtering and selected attributes");

  await page.click("#map-show-case");
  assert.equal(await page.$eval("#map-show-case",e=>e.hidden),true);
  assert.equal(await page.$eval("#map-show-recent",e=>e.hidden),false);
  assert.match(await page.$eval("#map-status",e=>e.textContent),/ARCHIVED CASE/);
  assert.match(await displayed(),/^3 /);
  assert.equal(await page.$eval(".map-legend",e=>e.textContent.includes("MODIS Aqua")),true);
  assert.equal(await page.$eval("#map-inspector-details",e=>e.textContent.includes("candidate association")),true);
  let mapPins=await page.evaluate(()=>({
   aqua:document.querySelectorAll(".map-pixel.case-modis").length,
   viirs:document.querySelectorAll(".map-pixel.case-viirs").length
  }));
  assert.deepEqual(mapPins,{aqua:1,viirs:2});
  assert.equal(archived.analysis.identity_confirmed,false);
  await page.click(".map-measurements summary");
  detail=await page.$eval("#map-inspector-details",e=>e.textContent);
  assert.match(detail,/107/);assert.match(detail,/18.62/);assert.match(detail,/5.53/);
  console.log("FIN-01: separate real NASA MODIS/VIIRS case, 3 markers and physical caveats");

  await page.click('[data-language="pt-BR"]');
  assert.match(await page.$eval("#map-status",e=>e.textContent),/CASO HISTÓRICO/);
  assert.match(await page.$eval("#map-inspector-details",e=>e.textContent),/associação candidata/i);
  assert.match(await page.$eval("#map-show-recent",e=>e.textContent),/Voltar às observações/);
  await page.click("#map-show-recent");
  assert.match(await displayed(),new RegExp("^"+(n20+n21)+" "));
  assert.equal(await page.$eval('[data-map-filter="all"]',e=>e.getAttribute("aria-pressed")),"true");
  await page.click("#map-point-list .map-list-point");
  assert.match(await page.$eval("#map-inspector-details",e=>e.textContent),/Um satélite identificou uma anomalia térmica/);
  await page.click('[data-language="en"]');
  assert.match(await page.$eval("#map-inspector-details",e=>e.textContent),/A satellite detected a thermal anomaly/);
  console.log("FIN-01: EN/PT-BR roundtrip retains real point and case/live separation");

  await page.click('[data-view="calendario"]');
  assert.equal(await page.$eval("#calendario",e=>e.classList.contains("hidden")),false);
  await page.waitForFunction(()=>document.querySelectorAll("#state-calendar .state-heat-cell:not(:disabled)").length===40,{timeout:30000});
  assert.equal(await page.$eval('[data-history-view="state"]',e=>e.getAttribute("aria-pressed")),"true");
  assert.match(await page.$eval("#calendario .section-lead",e=>e.textContent),/January|October|historical thermal/i);
  assert.equal(await page.$eval("#state-calendar .state-year-row",e=>e.textContent.includes("2023")),true);
  assert.equal(await page.evaluate(()=>document.querySelectorAll("#state-calendar .state-heat-cell:disabled").length),8);
  assert.match(await page.$eval("#state-calendar .year-partial",e=>e.textContent),/PARTIAL/);
  await page.click("#state-calendar .state-year-row:last-child .state-heat-cell:nth-child(10)");
  assert.match(await page.$eval("#state-calendar-detail",e=>e.textContent),/SEP\/2026.*MODIS Aqua.*3,518.*NRT/s);
  await page.click('[data-state-sensor="NOAA20"]');
  assert.match(await page.$eval("#state-calendar-detail",e=>e.textContent),/SEP\/2026.*VIIRS NOAA-20.*16,489.*NRT/s);
  await page.click('[data-state-sensor="Aqua"]');
  await page.click("#state-calendar .state-year-row:last-child .state-heat-cell:nth-child(9)");
  assert.match(await page.$eval("#state-calendar-detail",e=>e.textContent),/AUG\/2026.*MODIS Aqua.*2,153.*SP/s);
  await page.click('[data-state-sensor="NOAA20"]');
  assert.match(await page.$eval("#state-calendar-detail",e=>e.textContent),/AUG\/2026.*VIIRS NOAA-20.*10,451.*NRT/s);
  await page.click('[data-language="pt-BR"]');
  assert.match(await page.$eval("#state-calendar-detail",e=>e.textContent),/AGO\/2026.*VIIRS NOAA-20.*10\.451.*provisório/s);
  assert.match(await page.$eval('[data-history-view="state"]',e=>e.textContent),/Amazonas/);
  assert.match(await page.$eval("#state-calendar .year-partial",e=>e.textContent),/PARCIAL/);
  await page.click('[data-language="en"]');
  console.log("HIST-02: state SCI-03 2023–26 40 months, two sensors, SP/NRT, missing November/December, EN/PT-BR");

  await page.click('[data-history-view="pilot"]');
  assert.equal(await page.$eval("#pilot-history",e=>e.hidden),false);
  assert.equal(await page.$eval("#state-history",e=>e.hidden),true);
  await page.waitForSelector("#calendar .heat-cell:not([disabled])");
  await page.click("#calendar .heat-cell:not([disabled])");
  assert.match(await page.$eval("#calendar-detail",e=>e.textContent),/MODIS Aqua/);
  assert.match(await page.$eval("#pilot-history",e=>e.textContent),/2022–2024/);
  await page.select("#region","B");
  assert.equal(await page.$eval("#region",e=>e.value),"B");
  await page.click('[data-history-view="state"]');
  assert.equal(await page.$eval("#state-history",e=>e.hidden),false);
  assert.equal(await page.$eval("#pilot-history",e=>e.hidden),true);
  console.log("HIST-02: pilot A/B stays independent and selectable; statewide remains primary");

  await page.click('[data-view="ciencia"]');
  assert.match(await page.$eval(".explain-first",e=>e.textContent),/not a confirmed fire/i);
  assert.match(await page.$eval(".explain-first",e=>e.textContent),/50.73%/);
  assert.equal(await page.$eval("#science-method",e=>e.open),false);
  await page.click("#science-method summary");
  assert.equal(await page.$eval("#validation-chart",e=>e.children.length>0),true);
  console.log("FIN-01: original 2022–24 calendar and transparent historical methodology preserved");

  await page.click('[data-view="agora"]');
  await page.setViewport({width:390,height:844});
  await new Promise(resolve=>setTimeout(resolve,450));
  const geo=await page.evaluate(()=>({
   map:document.querySelector("#fire-map").getBoundingClientRect().width,
   wrap:document.querySelector(".map-explorer").getBoundingClientRect().width,
   h:document.querySelector("#fire-map").getBoundingClientRect().height,
   horizontalOverflow:document.documentElement.scrollWidth-innerWidth
  }));
  assert.ok(geo.wrap<=390&&geo.map>270&&geo.map<=geo.wrap&&geo.h>=300,"mobile map layout");
  assert.ok(geo.horizontalOverflow<20,"no horizontal page overflow");
  await page.click("#map-show-case");
  assert.match(await page.$eval("#map-case-disclosure",e=>e.textContent),/separate from|not part of/i);
  await page.click("#map-show-recent");
  console.log("FIN-01: responsive 390x844 and historical layer switch on mobile");

  assert.deepEqual(errors,[],"no uncaught JS exceptions");
  await page.setRequestInterception(true);
  page.on("request",req=>{
   if(req.url().includes("/data/recente.json"))req.respond({status:200,contentType:"application/json",body:JSON.stringify({status:"unavailable",detections:[],last_success_utc:null})});
   else req.continue();
  });
  await page.reload({waitUntil:"domcontentloaded"});
  await page.waitForFunction(()=>document.querySelector("#map-status").textContent.includes("No available NASA detections"));
  assert.equal(await page.$eval("#map-point-list",e=>e.children.length),0);
  assert.equal(await page.$eval("#map-no-data",e=>e.hidden),false);
  await page.waitForFunction(()=>!document.querySelector("#map-show-case").disabled);
  await page.click("#map-show-case");
  assert.match(await page.$eval("#map-status",e=>e.textContent),/ARCHIVED CASE/);
  console.log("FIN-01: unavailable recent source does not mislabel historical case as live");
 }finally{await browser.close();}
}
run().catch(e=>{console.error(e);process.exitCode=1;});
