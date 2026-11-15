/* HIST-02: pure frontend projection of versioned SCI-03 state data. Does NOT modify science. */
(function(root,factory){
 const lib=factory();
 if(typeof module==="object"&&module.exports)module.exports=lib;
 if(root)root.FireLensHistory=lib;
})(typeof globalThis!=="undefined"?globalThis:this,function(){
 "use strict";
 const YEARS=[2023,2024,2025,2026],SENSORS=["Aqua","NOAA20"];
 const COLUMNS=["year","month","sensor","cell_south_lat","cell_west_lon","pixels"];
 function processing(year,month,sensor){
  if(!YEARS.includes(year)||!SENSORS.includes(sensor)||!Number.isInteger(month)||month<1||month>12)return null;
  if(month>10)return null; // not in this SCI-03 aggregation, even if other archives exist
  if(year<2026)return "archive"; // Brazil annual FIRMS country CSV; do not assert SP processing
  if(month<=7)return "SP";
  if(month===8)return sensor==="Aqua"?"SP":"NRT";
  return "NRT"; // September / October
 }
 function derive(source){
  if(!source||source.id!=="SCI-03"||JSON.stringify(source.columns)!==JSON.stringify(COLUMNS)||
    !Array.isArray(source.rows))throw Error("SCI-03 history format unavailable");
  const groups=new Map(),seen=new Set();
  for(const row of source.rows){
   if(!Array.isArray(row)||row.length!==6)throw Error("Invalid SCI-03 row");
   const [year,month,sensor,lat,lon,pixels]=row;
   if(!YEARS.includes(year)||!SENSORS.includes(sensor)||!Number.isInteger(month)||month<1||month>10||
      !Number.isInteger(lat)||!Number.isInteger(lon)||!Number.isSafeInteger(pixels)||pixels<0)
      throw Error("Invalid SCI-03 cell");
   const rowId=[year,month,sensor,lat,lon].join("/");
   if(seen.has(rowId))throw Error("Duplicate SCI-03 cell");
   seen.add(rowId);
   const key=year+"/"+month+"/"+sensor;
   groups.set(key,(groups.get(key)||0)+pixels);
  }
  const months=[];
  for(const year of YEARS)for(let month=1;month<=12;month++)for(const sensor of SENSORS){
   const key=year+"/"+month+"/"+sensor;
   const available=month<=10&&groups.has(key); // absent != observed zero; never invent coverage
   months.push({year,month,sensor,available,pixels:available?groups.get(key):null,
                processing:available?processing(year,month,sensor):null});
  }
  return {months,sourceId:source.id,scope:"Amazonas simplified state polygon; 1-degree grid × UTC month",
          sensorCounts:"pixel detections, not individual fires"};
 }
 function getMonth(state,year,month,sensor){
  return state?.months?.find(x=>x.year===year&&x.month===month&&x.sensor===sensor)||null;
 }
 return {YEARS,SENSORS,COLUMNS,processing,derive,getMonth};
});
