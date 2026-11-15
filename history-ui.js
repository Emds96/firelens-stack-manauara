/* HIST-02: isolated, bilingual Amazonas SCI-03 calendar. Pilot A/B remains in app.js. */
(function(){
"use strict";
const H=window.FireLensHistory,$=s=>document.querySelector(s);
if(!H||!$("#state-calendar")||!$("#pilot-history"))return;
const words={
 en:{
  mainTitle:"Historical thermal detections in Amazonas",
  mainSubtitle:"January–October 2023–2026 · exploratory statewide monthly observations, not confirmed individual fires.",
  "mode.aria":"Choose a historical dataset",
  "mode.state":"Amazonas · 2023–2026","mode.pilot":"Pilot regions A/B · 2022–2024",
  "state.aria":"Amazonas monthly history",
  "state.title":"Amazonas · monthly satellite detections",
  "state.scope":"Simplified state boundary · 1° cells, aggregated by UTC month · January–October only.",
  "sensor.label":"Choose a satellite","sensor.aria":"Select the historical satellite",
  provenance:"2023–2025: annual Brazil FIRMS archive. 2026: Jan–Jul SP/SP; August Aqua SP and NOAA-20 NRT; Sep–Oct NRT/NRT. NRT is provisional.",
  loading:"Loading Amazonas monthly observations…",error:"Amazonas SCI-03 data unavailable. The separate pilot calendar remains accessible.",
  legend:"Fewer → more detected pixels (selected sensor only)",
  "unavailable.legend":"— = unavailable in this series, not zero fires",
  "detail.default":"Select a month to see its original pixel count and source.",
  "detail.unavailable":"Unavailable in this dataset. This is not evidence that no fire occurred.",
  caveat:"2026 is partial. November and December are not present in this January–October dataset for any year. SP and NRT have different processing and attributes. Counts from the two satellites should not be equated or interpreted as individual fires.",
  "pilot.aria":"Separate experiment for pilot regions A and B",
  "pilot.kicker":"SEPARATE EXPERIMENT · 2022–2024",
  "pilot.title":"Experimental A/B regions — not all of Amazonas",
  "pilot.subtitle":"Different geometry, filters and periods. Do not merge this calendar with the statewide SCI-03 series.",
  partial:"PARTIAL",count:"detected thermal-anomaly pixels",
  archive:"Annual Brazil FIRMS archive",sp:"SP (standard processing)",nrt:"NRT (provisional, subject to revision)",
  source:"Source",notComparable:"Original detections only; not corrected to match the other sensor, and not individual fires.",
  shortArchive:"ARCHIVE",unavailable:"Unavailable"
 },
 "pt-BR":{
  mainTitle:"Histórico de detecções térmicas no Amazonas",
  mainSubtitle:"Janeiro–outubro de 2023–2026 · observações mensais estaduais exploratórias, não incêndios individuais confirmados.",
  "mode.aria":"Escolha a série histórica",
  "mode.state":"Amazonas · 2023–2026","mode.pilot":"Regiões-piloto A/B · 2022–2024",
  "state.aria":"Histórico mensal do estado do Amazonas",
  "state.title":"Amazonas · detecções mensais por satélite",
  "state.scope":"Contorno estadual simplificado · células de 1° agregadas por mês UTC · somente janeiro–outubro.",
  "sensor.label":"Escolha um satélite","sensor.aria":"Selecione o satélite histórico",
  provenance:"2023–2025: arquivo anual FIRMS Brasil. 2026: jan–jul SP/SP; agosto Aqua SP e NOAA-20 NRT; set–out NRT/NRT. NRT é provisório.",
  loading:"Carregando observações mensais do Amazonas…",error:"Dados SCI-03 do Amazonas indisponíveis. O calendário A/B separado continua acessível.",
  legend:"Menos → mais pixels detectados (somente o satélite selecionado)",
  "unavailable.legend":"— = indisponível nesta série, não zero incêndios",
  "detail.default":"Selecione um mês para ver a contagem original e sua fonte.",
  "detail.unavailable":"Indisponível neste arquivo. Isso não comprova ausência de fogo.",
  caveat:"2026 é parcial. Novembro e dezembro não estão disponíveis nesta série de janeiro a outubro para nenhum ano. SP e NRT diferem em processamento e atributos. As contagens dos dois satélites não devem ser igualadas nem interpretadas como incêndios individuais.",
  "pilot.aria":"Experimento separado para as regiões-piloto A e B",
  "pilot.kicker":"EXPERIMENTO SEPARADO · 2022–2024",
  "pilot.title":"Recortes experimentais A/B — não todo o Amazonas",
  "pilot.subtitle":"Geometria, filtros e períodos diferentes. Não misture este calendário com a série estadual SCI-03.",
  partial:"PARCIAL",count:"pixels com anomalia térmica detectados",
  archive:"Arquivo anual FIRMS Brasil",sp:"SP (processamento padrão)",nrt:"NRT (provisório, sujeito a revisão)",
  source:"Fonte",notComparable:"Somente detecções originais, sem correção entre sensores e sem equivalência com incêndios individuais.",
  shortArchive:"ARQUIVO",unavailable:"Indisponível"
 }
};
const months={en:["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"],
 "pt-BR":["JAN","FEV","MAR","ABR","MAI","JUN","JUL","AGO","SET","OUT","NOV","DEZ"]};
let lang="en",data=null,failed=false,view="state",sensor="Aqua",selection=null;
function t(key){return words[lang][key]||key;}
function fmt(n){return new Intl.NumberFormat(lang).format(n);}
function statusText(p){return p==="SP"?t("sp"):p==="NRT"?t("nrt"):t("archive");}
function localized(){
 for(const el of document.querySelectorAll("[data-hist-t]"))el.textContent=t(el.dataset.histT);
 for(const el of document.querySelectorAll("[data-hist-aria]"))el.setAttribute("aria-label",t(el.dataset.histAria));
}
function setView(next){
 view=next==="pilot"?"pilot":"state";
 $("#state-history").hidden=view!=="state";
 $("#pilot-history").hidden=view!=="pilot";
 for(const b of document.querySelectorAll("[data-history-view]"))
  b.setAttribute("aria-pressed",String(b.dataset.historyView===view));
 // Legacy A/B calendar is loaded, rendered and translated only by app.js.
 if(view==="state")render();
}
function detail(month){
 const target=$("#state-calendar-detail");
 if(!month){target.textContent=t("detail.default");return;}
 const label=months[lang][month.month-1]+"/"+month.year;
 const sat=month.sensor==="Aqua"?"MODIS Aqua":"VIIRS NOAA-20";
 target.textContent=month.available?
  label+" · "+sat+": "+fmt(month.pixels)+" "+t("count")+". "+t("source")+
  ": "+statusText(month.processing)+". "+t("notComparable"):
  label+" · "+sat+": "+t("detail.unavailable");
}
function render(){
 localized();
 for(const b of document.querySelectorAll("[data-state-sensor]"))
  b.setAttribute("aria-pressed",String(b.dataset.stateSensor===sensor));
 const host=$("#state-calendar");
 if(!data){
  const e=document.createElement("div");e.className="empty";
  e.textContent=t(failed?"error":"loading");host.replaceChildren(e);
  detail(null);return;
 }
 const active=data.months.filter(m=>m.sensor===sensor&&m.available);
 const max=Math.max(1,...active.map(m=>m.pixels));
 const wrap=document.createDocumentFragment(),header=document.createElement("div");
 header.className="month-top";
 header.append(document.createElement("span"));
 for(const abbr of months[lang]){const el=document.createElement("span");el.textContent=abbr;header.append(el);}
 wrap.append(header);
 for(const year of H.YEARS){
  const row=document.createElement("div");row.className="year-row state-year-row";
  const yearLabel=document.createElement("strong");yearLabel.className="year-label";yearLabel.textContent=String(year);
  if(year===2026){
   yearLabel.classList.add("year-partial");
   const flag=document.createElement("small");flag.textContent=t("partial");yearLabel.append(flag);
  }
  row.append(yearLabel);
  for(let mon=1;mon<=12;mon++){
   const record=H.getMonth(data,year,mon,sensor);
   const b=document.createElement("button");b.type="button";b.className="heat-cell state-heat-cell";
   if(record&&record.available){
    const intensity=Math.sqrt(record.pixels/max);
    b.style.background="hsl("+(167-intensity*137)+" "+(30+intensity*49)+"% "+(19+intensity*30)+"%)";
    const count=document.createElement("strong");count.textContent=fmt(record.pixels);
    const badge=document.createElement("small");badge.textContent=year===2026?record.processing:t("shortArchive");
    b.append(count,badge);
    b.title=months[lang][mon-1]+"/"+year+" · "+(sensor==="Aqua"?"MODIS Aqua":"VIIRS NOAA-20")+
       ": "+fmt(record.pixels)+" "+t("count")+" · "+statusText(record.processing);
    b.setAttribute("aria-label",b.title);
    if(selection&&selection.year===year&&selection.month===mon)b.classList.add("active");
    b.addEventListener("click",()=>{
     selection={year,month:mon};
     for(const e of host.querySelectorAll(".state-heat-cell.active"))e.classList.remove("active");
     b.classList.add("active");detail(record);
    });
   }else{
    b.classList.add("state-unavailable");b.textContent="—";b.disabled=true;
    b.title=months[lang][mon-1]+"/"+year+": "+t("detail.unavailable");
    b.setAttribute("aria-label",b.title);
   }
   row.append(b);
  }
  wrap.append(row);
 }
 host.replaceChildren(wrap);
 const selected=selection?H.getMonth(data,selection.year,selection.month,sensor):null;
 detail(selected);
}
for(const b of document.querySelectorAll("[data-history-view]"))
 b.addEventListener("click",()=>setView(b.dataset.historyView));
for(const b of document.querySelectorAll("[data-state-sensor]"))
 b.addEventListener("click",()=>{sensor=b.dataset.stateSensor;render();});
document.addEventListener("firelens:language",e=>{
 lang=e.detail==="pt-BR"?"pt-BR":"en";render();
});
setView("state");render();
fetch("data/sci03_agregados.json",{cache:"no-store"}).then(r=>{
 if(!r.ok)throw Error("SCI-03 unavailable");
 return r.json();
}).then(source=>{
 data=H.derive(source);failed=false;render();
}).catch(()=>{
 data=null;failed=true;render();
});
})();