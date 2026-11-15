"use strict";
const {test}=require("node:test"),assert=require("node:assert/strict"),fs=require("node:fs");
const recent=JSON.parse(fs.readFileSync("data/recente.json","utf8"));
const caseData=JSON.parse(fs.readFileSync("data/caso_visao_aguia_20261110.json","utf8"));
const source=JSON.parse(fs.readFileSync("data/test02_observacoes_20261110_14.json","utf8"));
const results=JSON.parse(fs.readFileSync("data/test02_resultados.json","utf8"));
test("Eagle case is a dated, isolated research layer, never current NOAA20/NOAA21 NRT",()=>{
 assert.equal(caseData.status,"historical_case_not_live");
 assert.equal(caseData.date_utc,"2026-11-10");
 assert.equal(caseData.analysis.identity_confirmed,false);
 assert.equal(caseData.records.length,3);
 assert.equal(caseData.records.filter(x=>x.satellite==="Aqua").length,1);
 assert.equal(caseData.records.filter(x=>x.satellite==="NOAA-20").length,2);
 assert.ok(recent.detections.every(x=>x.sensor==="NOAA20"||x.sensor==="NOAA21"));
});
test("all curated physical measurements exactly reproduce the NASA source JSON",()=>{
 for(const r of caseData.records){
  const candidates=r.id.startsWith("M")?source.MODIS_NRT:source.VIIRS_NOAA20_NRT;
  const original=candidates.find(x=>x.id===r.id);
  assert.ok(original,r.id);
  for(const [k,v] of Object.entries(r))assert.deepEqual(v,original[k],r.id+"."+k);
 }
});
test("107 minutes, 18.62 MW, 13.09 MW, T31/TI5 and differences are source-derived",()=>{
 const mod=caseData.records.find(x=>x.satellite==="Aqua");
 const viirs=caseData.records.filter(x=>x.satellite==="NOAA-20");
 const t=Math.abs(Date.parse(mod.time_utc)-Date.parse(viirs[0].time_utc))/60000;
 const total=viirs.reduce((n,x)=>n+x.frp_mw,0);
 assert.equal(t,107);assert.equal(caseData.analysis.delta_minutes,t);
 assert.equal(mod.frp_mw,18.62);assert.equal(total,13.09);
 assert.equal(caseData.analysis.viirs_frp_sum_mw,total);
 assert.ok(Math.abs(caseData.analysis.frp_difference_mw-(mod.frp_mw-total))<1e-8);
 assert.ok(Math.abs(caseData.analysis.viirs_to_modis_frp_ratio-(total/mod.frp_mw))<.0006);
 const mean=viirs.reduce((n,x)=>n+x.t11_k,0)/2;
 assert.ok(Math.abs(mean-caseData.analysis.viirs_ti5_mean_k)<.001);
 assert.ok(Math.abs(Math.abs(mod.t11_k-mean)-caseData.analysis.t11_brightness_difference_k)<.001);
 assert.equal(caseData.analysis.spatial_approximate,true);
 const group=results.group_diagnostics.find(x=>x.modis_id===mod.id);
 assert.ok(group&&group.four_locks_candidate_8k);
 assert.deepEqual(group.in_box_and_within_120min_ids,viirs.map(x=>x.id));
});
test("11-Nov independent observation control is not misrepresented as a matching case",()=>{
 const d=results.daily.find(x=>x.date_utc==="2026-11-11");
 assert.equal(d.eligible_diurnal_modis_aqua,12);
 assert.equal(d.eligible_diurnal_noaa20,222);
 assert.equal(d.four_locks_candidate_groups_8k,0);
});
