"use strict";
const {test}=require("node:test"),assert=require("node:assert/strict"),fs=require("node:fs");
const m=require("../map-data.js");
const p={latitude:-3.12,longitude:-60.02,sensor:"NOAA20",confidence:"n",daynight:"N",observed_at_utc:"2026-11-14T05:48:00Z"};
test("coordinates and actual attributes are preserved without inventing area",()=>{
 const d=m.detection(p,7);
 assert.equal(d.lat,-3.12);assert.equal(d.lon,-60.02);assert.equal(d.id,7);
 assert.equal(d.confidence,"n");assert.equal(d.daynight,"N");
 assert.equal(d.burned_area,undefined);
});
test("invalid sensor, timestamps and coordinates are rejected",()=>{
 for(const x of [{...p,latitude:91},{...p,longitude:181},{...p,latitude:null},{...p,sensor:"MODIS"},{...p,observed_at_utc:"not-date"}])assert.equal(m.detection(x,0),null);
});
test("filters separate NOAA20 NOAA21 without duplicating",()=>{
 const a=m.detection(p,0),b=m.detection({...p,sensor:"NOAA21"},1);
 assert.equal(m.filter([a,b],"NOAA20").length,1);
 assert.equal(m.filter([a,b],"NOAA21")[0].sensor,"NOAA21");
 assert.equal(m.filter([a,b],"all").length,2);
});
test("unavailable and old snapshots are always stale, empties stay empty",()=>{
 const now=Date.parse("2026-11-14T18:00:00Z");
 let s=m.derive({status:"ok",last_success_utc:"2026-11-14T17:00:00Z",detections:[p]},now);
 assert.equal(s.available,true);assert.equal(s.stale,false);
 s=m.derive({status:"ok",last_success_utc:"2026-11-14T12:00:00Z",detections:[p]},now);
 assert.equal(s.stale,true);
 s=m.derive({status:"unavailable",last_success_utc:"2026-11-14T17:00:00Z",detections:[p]},now);
 assert.equal(s.available,false);assert.equal(s.stale,true);assert.equal(s.points.length,1);
 s=m.derive({status:"unavailable",detections:[]},now);
 assert.equal(s.points.length,0);assert.equal(s.stale,true);
});
test("public FIRMS JSON uses real valid positions only",()=>{
 const d=JSON.parse(fs.readFileSync("data/recente.json","utf8")),s=m.derive(d);
 assert.equal(s.points.length+s.rejected,(d.detections||[]).length);
 assert.equal(s.sensor20+s.sensor21,s.points.length);
 assert.ok(s.points.every(x=>Number.isFinite(x.lat)&&Number.isFinite(x.lon)));
});