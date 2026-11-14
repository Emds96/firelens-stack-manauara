/* MAP-01: pure, testable NASA FIRMS coordinate and status logic. */
(function(root,factory){
  const lib=factory();
  if(typeof module==="object"&&module.exports)module.exports=lib;
  if(root)root.FireLensMapData=lib;
})(typeof globalThis!=="undefined"?globalThis:this,function(){
  "use strict";
  function detection(r,i){
    if(!r||typeof r!=="object")return null;
    if(r.latitude===null||r.longitude===null||r.latitude===""||r.longitude==="")return null;
    const lat=Number(r.latitude),lon=Number(r.longitude);
    if(!Number.isFinite(lat)||!Number.isFinite(lon)||Math.abs(lat)>90||Math.abs(lon)>180)return null;
    if(r.sensor!=="NOAA20"&&r.sensor!=="NOAA21")return null;
    if(!r.observed_at_utc||!Number.isFinite(Date.parse(r.observed_at_utc)))return null;
    return {id:i,lat,lon,sensor:r.sensor,observed:r.observed_at_utc,
      confidence:String(r.confidence??"?"),daynight:String(r.daynight??"?")};
  }
  function derive(raw,now=Date.now()){
    raw=raw&&typeof raw==="object"?raw:{};
    const observations=Array.isArray(raw.detections)?raw.detections:[];
    const points=observations.map(detection).filter(Boolean);
    const t=Date.parse(raw.last_success_utc||"");
    const available=raw.status==="ok"&&Number.isFinite(t);
    return {points,rejected:observations.length-points.length,
      sensor20:points.filter(x=>x.sensor==="NOAA20").length,
      sensor21:points.filter(x=>x.sensor==="NOAA21").length,
      available,stale:!available||now-t>14400000||t>now+300000,
      lastSuccess:raw.last_success_utc||null,lastObservation:raw.last_observation_utc||null};
  }
  function filter(points,sensor){return sensor==="NOAA20"||sensor==="NOAA21"?points.filter(x=>x.sensor===sensor):points.slice();}
  return {detection,derive,filter};
});