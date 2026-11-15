"use strict";
/* HIST-02 source integrity and coverage checks against versioned SCI-03 NASA data. */
const {test}=require("node:test"),assert=require("node:assert/strict"),fs=require("node:fs");
const H=require("../history-state.js");
const original=JSON.parse(fs.readFileSync("data/sci03_agregados.json","utf8"));
const state=H.derive(original);
function sum(y,s){return state.months.filter(x=>x.year===y&&x.sensor===s&&x.available).reduce((n,x)=>n+x.pixels,0)}
test("statewide SCI-03 is not pilot A/B and preserves actual 1-degree cells and pixel counts",()=>{
 assert.equal(original.id,"SCI-03");
 assert.equal(original.rows.length,4434);
 assert.deepEqual(original.columns,H.COLUMNS);
 assert.deepEqual(H.YEARS,[2023,2024,2025,2026]);
 assert.deepEqual(H.SENSORS,["Aqua","NOAA20"]);
 assert.equal(state.months.length,4*12*2);
 assert.deepEqual([sum(2023,"Aqua"),sum(2023,"NOAA20")],[17468,70276]);
 assert.deepEqual([sum(2024,"Aqua"),sum(2024,"NOAA20")],[22300,87776]);
 assert.deepEqual([sum(2025,"Aqua"),sum(2025,"NOAA20")],[3941,19017]);
 assert.deepEqual([sum(2026,"Aqua"),sum(2026,"NOAA20")],[8002,42636]);
});
test("each sensor has precisely January-October for all four years; unavailable is null, never zero",()=>{
 for(const year of H.YEARS)for(const sensor of H.SENSORS){
  const months=state.months.filter(x=>x.year===year&&x.sensor===sensor);
  assert.deepEqual(months.filter(x=>x.available).map(x=>x.month),[1,2,3,4,5,6,7,8,9,10]);
  for(const x of months.filter(x=>!x.available)){
   assert.ok([11,12].includes(x.month));assert.equal(x.pixels,null);
   assert.equal(x.processing,null);
  }
 }
 assert.equal(H.getMonth(state,2026,9,"Aqua").pixels,3518);
 assert.equal(H.getMonth(state,2026,9,"NOAA20").pixels,16489);
});
test("2026 source processing differs by sensor and calendar month; archive is not falsely labeled SP",()=>{
 for(const sensor of H.SENSORS){
  for(let month=1;month<=7;month++)assert.equal(H.processing(2026,month,sensor),"SP");
  for(const month of [9,10])assert.equal(H.processing(2026,month,sensor),"NRT");
 }
 assert.equal(H.processing(2026,8,"Aqua"),"SP");
 assert.equal(H.processing(2026,8,"NOAA20"),"NRT");
 for(const year of [2023,2024,2025])for(const sensor of H.SENSORS)
  assert.equal(H.processing(year,8,sensor),"archive");
 assert.equal(H.processing(2026,11,"Aqua"),null);
 assert.equal(H.processing(2026,12,"NOAA20"),null);
});
test("sparse source never invents zero detection or full coverage",()=>{
 const sparse={...original,rows:original.rows.filter(row=>!(row[0]===2024&&row[1]===2&&row[2]==="Aqua"))};
 const state2=H.derive(sparse);
 assert.equal(H.getMonth(state2,2024,2,"Aqua").available,false);
 assert.equal(H.getMonth(state2,2024,2,"Aqua").pixels,null);
 assert.equal(H.getMonth(state2,2024,2,"NOAA20").available,true);
});
test("invalid, duplicate or modified SCI-03 schema fails safe",()=>{
 assert.throws(()=>H.derive({...original,id:"pilot"}));
 assert.throws(()=>H.derive({...original,columns:["year","month"],rows:[]}));
 assert.throws(()=>H.derive({...original,rows:[original.rows[0],original.rows[0]]}),/Duplicate/);
 assert.throws(()=>H.derive({...original,rows:[[2026,11,"NOAA20",-3,-60,3]]}),/Invalid/);
 assert.throws(()=>H.derive({...original,rows:[[2023,1,"Aqua",-3,-60,-1]]}),/Invalid/);
});
