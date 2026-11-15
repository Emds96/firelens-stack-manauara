/* MAP-01: interactive, bilingual, point-level NASA FIRMS translator. */
(function(){
"use strict";
const $=s=>document.querySelector(s),D=window.FireLensMapData;
if(!D||!$("#fire-map"))return;
const i18n={
 en:{listTitle:"Select a detection",listPrev:"Previous",listNext:"Next",listRange:"of",heading:"Explore recent satellite detections",explain:"Click a marker to inspect a real NASA FIRMS detection. A point is not a confirmed individual fire or a burned-area polygon.",all:"Both satellites",filter:"Filter satellites",loaded:"visible detections",select:"Select a satellite marker for its scientific and human explanations.",source:"NASA FIRMS Area API",statusOK:"Source retrieved",statusOld:"Outdated snapshot — not current",statusFailed:"Source unavailable — earlier snapshot",statusEmpty:"No available NASA detections",updated:"Latest successful retrieval",observed:"Latest returned observation",stale:"The last retrieval is over four hours old.",previous:"The current retrieval failed; markers, if present, belong to an earlier snapshot.",latency:"A recent retrieval does not imply a recent satellite observation.",border:"The simplified Amazonas boundary has not been verified against the official IBGE geometry.",noPoint:"There are no verified coordinates to display; this does not mean there were no fires.",noMatch:"No detections match the selected satellite.",libError:"Map library unavailable. Other FireLens features remain available.",tileError:"Background tiles could not load; coordinate data remains available.",clusterNote:"Nearby markers are clustered. Zoom in to inspect individual detections.",clusterFail:"Clustering unavailable; individual markers are displayed.",science:"Scientific translator",human:"Human translator",satellite:"Satellite",coords:"Coordinates (lat, lon)",time:"Observation time (Manaus)",confidence:"Reported confidence",daynight:"Day / night",day:"Daytime",night:"Nighttime",normal:"Normal (n)",high:"High (h)",unknown:"Not specified",scienceDesc:"Coordinates indicate a detected pixel, not the size of a fire. NASA FIRMS confidence is a sensor category, not a probability that a fire occurred.",humanIntro:"Satellite",humanObserved:"detected a",humanConfidence:"confidence thermal anomaly during",humanEnding:"at this location and observation time. This is a pixel-level thermal signal, not proof of an individual fire or its burned area.",footer:"Map background: © OpenStreetMap contributors. NASA FIRMS provides observation points, not burned-area shapes."},
 "pt-BR":{listTitle:"Selecione uma detecção",listPrev:"Anterior",listNext:"Próxima",listRange:"de",heading:"Explore as detecções recentes no mapa",explain:"Clique em um marcador para consultar uma detecção real NASA FIRMS. Um ponto não é um incêndio individual confirmado nem um polígono de área queimada.",all:"Ambos os satélites",filter:"Filtrar satélites",loaded:"detecções visíveis",select:"Selecione um marcador para ver as explicações científica e humana.",source:"NASA FIRMS Area API",statusOK:"Fonte consultada",statusOld:"Captura desatualizada — não é atual",statusFailed:"Fonte indisponível — captura anterior",statusEmpty:"Sem detecções NASA disponíveis",updated:"Última consulta bem-sucedida",observed:"Última observação retornada",stale:"A última consulta ocorreu há mais de quatro horas.",previous:"A consulta atual falhou; os marcadores, se presentes, são de uma captura anterior.",latency:"Uma consulta recente não significa uma observação recente do satélite.",border:"O contorno simplificado do Amazonas ainda não foi conferido com a geometria oficial do IBGE.",noPoint:"Não há coordenadas verificadas para exibir; isso não significa ausência de incêndios.",noMatch:"Nenhuma detecção corresponde ao satélite selecionado.",libError:"Biblioteca do mapa indisponível. As outras funções do FireLens continuam acessíveis.",tileError:"Mapa-base não carregou; as coordenadas continuam disponíveis.",clusterNote:"Marcadores próximos são agrupados. Amplie o zoom para explorar os pontos.",clusterFail:"O agrupamento não carregou; os pontos individuais são exibidos.",science:"Tradutor científico",human:"Tradutor humano",satellite:"Satélite",coords:"Coordenadas (lat, lon)",time:"Horário da observação (Manaus)",confidence:"Confiança informada",daynight:"Dia / noite",day:"Diurna",night:"Noturna",normal:"Normal (n)",high:"Alta (h)",unknown:"Não especificado",scienceDesc:"As coordenadas indicam um pixel detectado, não o tamanho do incêndio. A confiança NASA FIRMS é uma categoria do sensor, não uma probabilidade de ter ocorrido incêndio.",humanIntro:"O satélite",humanObserved:"registrou uma anomalia térmica de confiança",humanConfidence:"no período",humanEnding:"neste local e horário. Trata-se de um sinal térmico em um pixel, não uma confirmação de incêndio individual nem de sua área queimada.",footer:"Mapa-base: © colaboradores do OpenStreetMap. NASA FIRMS fornece pontos de observação, não polígonos de área queimada."}
};
let lang="en",filter="all",map=null,layer=null,caseLayer=null,state=null,selected=null,caseStudy=null,caseSelected=null,mode="recent",firstView=true,caseFitted=false,tileErrors=0,canCluster=false,page=0;
let markerRefs=new Map();
const extra={
 en:{
  caseAction:"Explore a real case · Eagle's View",backRecent:"← Return to recent observations",
  browsePoints:"Browse detections in a list",caseTitle:"Eagle's View · real observations from 10 Nov 2026",
  caseStatus:"ARCHIVED CASE · NOT LIVE",caseBanner:"Historical research · 10 November 2026 · MODIS Aqua + VIIRS NOAA-20 · not part of the current satellite layer.",
  caseExplain:"Three thermal-anomaly pixels from two satellites were observed near one another 107 minutes apart. They may be related, but this does not confirm a single fire.",
  caseSource:"Real NASA FIRMS NRT observations · 10 Nov 2026",caseSummary:"One MODIS Aqua pixel and two nearby VIIRS NOAA-20 pixels, 107 minutes apart.",
  caseCount:"historical observations",caseNotReady:"The archived case could not load. Recent NASA detections remain available.",
  moreDetails:"Measurement details and scientific limits",humanTop:"A satellite detected a thermal anomaly at this location and time. It may indicate a heat source, but alone does not confirm an individual fire or its burned area.",
  caseHuman:"MODIS Aqua and VIIRS NOAA-20 observed nearby thermal signals at different times. This is a candidate association, NOT a confirmed single fire.",
  caseCaveat:"Pixel dimensions are approximate, not exact orbital footprints. T31 and TI5 are brightness temperatures in distinct channels. FRP is radiative power, not conserved energy.",
  t4:"~4 µm channel brightness (K)",t11:"~11 µm channel brightness (K)",
  pixels:"Approximate pixel dimensions",area:"Approximate scan × track area",frp:"Fire radiative power (MW)",caseDifference:"FRP difference (MW)",caseIntervals:"Observation gap (minutes)",
  caseResearch:"See the documented experiment",caseRaw:"See original observations",caseNotProof:"Nearby points are not a fire-identity confirmation.",
  sourceInfo:"Original NASA FIRMS record",eagleLegendModis:"MODIS Aqua · 10 Nov",eagleLegendViirs:"VIIRS NOAA-20 · 10 Nov"
 },
 "pt-BR":{
  caseAction:"Explorar um caso real · Visão da Águia",backRecent:"← Voltar às observações recentes",
  browsePoints:"Ver detecções em lista",caseTitle:"Visão da Águia · observações reais de 10/11/2026",
  caseStatus:"CASO HISTÓRICO · NÃO ATUAL",caseBanner:"Pesquisa histórica · 10/11/2026 · MODIS Aqua + VIIRS NOAA-20 · separada da camada recente.",
  caseExplain:"Três pixels com anomalias térmicas foram observados próximos por dois satélites com 107 minutos de intervalo. Podem estar relacionados, mas isso não confirma um incêndio único.",
  caseSource:"Observações reais NASA FIRMS NRT · 10/11/2026",caseSummary:"Um pixel MODIS Aqua e dois pixels VIIRS NOAA-20 próximos, com intervalo de 107 minutos.",
  caseCount:"observações históricas",caseNotReady:"Não foi possível carregar o caso histórico. As observações recentes continuam disponíveis.",
  moreDetails:"Ver medições e limites científicos",humanTop:"Um satélite identificou uma anomalia térmica neste local e horário. Isso pode indicar uma fonte de calor, mas não confirma isoladamente um incêndio nem a área queimada.",
  caseHuman:"MODIS Aqua e VIIRS NOAA-20 observaram sinais térmicos próximos em horários distintos. É uma associação candidata, NÃO a confirmação de um incêndio único.",
  caseCaveat:"As dimensões de pixel são aproximadas, não pegadas orbitais exatas. T31 e TI5 são temperaturas de brilho em canais distintos. FRP é potência radiativa, não energia conservada.",
  t4:"Temperatura de brilho no canal ~4 µm (K)",t11:"Temperatura de brilho no canal ~11 µm (K)",
  pixels:"Dimensões aproximadas do pixel",area:"Área aproximada scan × track",frp:"Potência radiativa (MW)",caseDifference:"Diferença de FRP (MW)",caseIntervals:"Intervalo entre observações (min)",
  caseResearch:"Consultar o experimento documentado",caseRaw:"Ver observações originais",caseNotProof:"Pontos próximos não confirmam a identidade de um incêndio.",
  sourceInfo:"Registro original NASA FIRMS",eagleLegendModis:"MODIS Aqua · 10/11",eagleLegendViirs:"VIIRS NOAA-20 · 10/11"
 }};
const t=k=>extra[lang]?.[k]||(i18n[lang]||i18n.en)[k]||k;
const num=(n,p=0)=>new Intl.NumberFormat(lang,{minimumFractionDigits:p,maximumFractionDigits:p}).format(n);
function time(x){if(!x||!Number.isFinite(Date.parse(x)))return "—";return new Intl.DateTimeFormat(lang,{dateStyle:"medium",timeStyle:"short",timeZone:"America/Manaus"}).format(new Date(x))+" AMT";}
function status(){
 if(mode==="case"){
  $("#map-status").textContent=t("caseStatus");
  $("#map-status").className="map-status map-status-old";
  $("#map-timestamps").textContent=t("caseSource")+" · "+
      time(caseStudy?.records?.[1]?.time_utc)+" → "+time(caseStudy?.records?.[0]?.time_utc);
  $("#map-notes").textContent=t("caseCaveat")+" "+t("caseNotProof");
  return;
 }
 if(!state)return;
 const isOld=state.stale;
 const label=!state.available?(state.points.length?t("statusFailed"):t("statusEmpty")):isOld?t("statusOld"):t("statusOK");
 $("#map-status").textContent=label;
 $("#map-status").className="map-status "+(isOld?"map-status-old":"map-status-ok");
 $("#map-timestamps").textContent=t("updated")+": "+time(state.lastSuccess)+" · "+t("observed")+": "+time(state.lastObservation);
 const notes=[!state.available&&state.points.length?t("previous"):state.stale?t("stale"):t("latency"),t("border")];
 $("#map-notes").textContent=notes.join(" ");
}
function field(label,value){
 const row=document.createElement("div");row.className="map-data-row";
 const a=document.createElement("dt"),b=document.createElement("dd");
 a.textContent=label;b.textContent=value;row.append(a,b);return row;
}
function legend(){
 const el=$(".map-legend");if(!el)return;
 el.replaceChildren();
 const items=mode==="case"?[["map-key case-modis",t("eagleLegendModis")],["map-key case-viirs",t("eagleLegendViirs")]]:
   [["map-key sensor20","NOAA-20"],["map-key sensor21","NOAA-21"]];
 for(const [cls,label] of items){
  const span=document.createElement("span"),key=document.createElement("i");
  key.className=cls;span.append(key,document.createTextNode(label));el.append(span);
 }
}
function technicalDetails(out,rows,source="NASA FIRMS"){
 const details=document.createElement("details");details.className="map-measurements";
 const summary=document.createElement("summary");summary.textContent=t("moreDetails");
 const dl=document.createElement("dl");dl.className="map-fields";
 for(const [label,value] of rows)dl.append(field(label,String(value)));
 const src=document.createElement("p");src.className="map-science-note";
 src.textContent=t("sourceInfo")+": "+source+". "+(mode==="case"?t("caseCaveat"):t("scienceDesc"));
 details.append(summary,dl,src);out.append(details);
}
function detail(p){
 const out=$("#map-inspector-details");out.replaceChildren();
 if(!p){
  out.classList.add("map-placeholder");
  out.textContent=mode==="case"?t("caseNotReady"):t("select");
  return;
 }
 out.classList.remove("map-placeholder");
 const intro=document.createElement("p");intro.className="map-unified";
 intro.textContent=mode==="case"?t("caseHuman"):t("humanTop");
 out.append(intro);
 const title=document.createElement("h4");
 title.textContent=(mode==="case"?p.satellite:(p.sensor==="NOAA20"?"NOAA-20":"NOAA-21"))+" · "+
   time(mode==="case"?p.time_utc:p.observed);
 out.append(title);
 if(mode==="case"){
  const a=caseStudy.analysis,n=num,rows=[
   [t("satellite"),p.satellite],[t("coords"),n(p.latitude,5)+", "+n(p.longitude,5)],
   [t("time"),time(p.time_utc)],[t("pixels"),n(p.scan_km,2)+" × "+n(p.track_km,2)+" km"],
   [t("area"),n(p.area_km2_approx,4)+" km²"],[t("t4"),n(p.t4_k,2)+" K"],
   [t("t11"),n(p.t11_k,2)+" K"],[t("frp"),n(p.frp_mw,2)+" MW"],
   [t("confidence"),p.confidence],[t("daynight"),p.daynight==="D"?t("day"):t("night")],
   [t("caseIntervals"),n(a.delta_minutes,0)],[t("caseDifference"),n(a.frp_difference_mw,2)+" MW"]];
  technicalDetails(out,rows,"NASA FIRMS MODIS_NRT / VIIRS_NOAA20_NRT");
  const link=document.createElement("a");link.href="docs/TEST-02_VISAO_AGUIA.md";
  link.target="_blank";link.rel="noopener noreferrer";link.textContent=t("caseResearch")+" ↗";link.className="map-nasa-link";
  out.append(link);
 }else{
  const sensor=p.sensor==="NOAA20"?"NOAA-20":"NOAA-21";
  const conf=p.confidence.toLowerCase()==="h"?t("high"):p.confidence.toLowerCase()==="n"?t("normal"):p.confidence;
  const daytime=p.daynight==="D"?t("day"):p.daynight==="N"?t("night"):t("unknown");
  technicalDetails(out,[[t("satellite"),sensor],
   [t("coords"),num(p.lat,5)+", "+num(p.lon,5)],[t("time"),time(p.observed)],
   [t("confidence"),conf],[t("daynight"),daytime]],"NASA FIRMS");
 }
}
function selectPoint(p,zoomToPoint){
 selected=p;detail(p);renderList();
 if(zoomToPoint&&map){
  // Recenter without markercluster.zoomToShowLayer: its async animation can
  // dereference a layer removed while filters/locale update the marker group.
  // Explicit setView is deterministic and preserves clickable markers.
  map.setView([p.lat,p.lon],Math.max(10,map.getZoom()),{animate:false});
 }
 $("#map-inspector-details").focus({preventScroll:true});
}
function updateModeControls(){
 $("#map-show-case").hidden=mode==="case";
 $("#map-show-recent").hidden=mode!=="case";
 $("#map-show-case").disabled=!caseStudy;
 $("#map-live-filters").hidden=mode==="case";
 $("#map-case-disclosure").hidden=mode!=="case";
 $("#map-case-disclosure").textContent=mode==="case"?t("caseBanner"):"";
 $("#map-section-title").textContent=t(mode==="case"?"caseTitle":"heading");
 const explanation=$('[data-map-t="explain"]');if(explanation)explanation.textContent=t(mode==="case"?"caseExplain":"explain");
 legend();
}
function selectCase(p,zoomToPoint){
 caseSelected=p;detail(p);renderList();
 if(zoomToPoint&&map)map.setView([p.latitude,p.longitude],Math.max(13,map.getZoom()),{animate:false});
 $("#map-inspector-details").focus({preventScroll:true});
}
function renderCase(){
 if(!caseStudy||mode!=="case")return;
 updateModeControls();status();
 $("#map-count").textContent=num(caseStudy.records.length)+" "+t("caseCount");
 $("#map-no-data").hidden=true;
 if(layer)layer.clearLayers();
 if(caseLayer)caseLayer.clearLayers();
 if(!caseSelected||!caseStudy.records.some(p=>p.id===caseSelected.id))caseSelected=caseStudy.records[0];
 detail(caseSelected);renderList();
 if(!map||!caseLayer)return;
 for(const p of caseStudy.records){
  const cls=p.satellite==="Aqua"?"case-modis":"case-viirs";
  const icon=L.divIcon({className:"map-pixel "+cls,html:"<span></span>",iconSize:[22,22],iconAnchor:[11,11]});
  const marker=L.marker([p.latitude,p.longitude],{icon,keyboard:true,title:p.satellite+" · "+time(p.time_utc)});
  marker.on("click",()=>selectCase(p,false));caseLayer.addLayer(marker);
 }
 if(!caseFitted){
  map.fitBounds(L.latLngBounds(caseStudy.records.map(p=>[p.latitude,p.longitude])).pad(.7),{maxZoom:13,animate:false});
  caseFitted=true;
 }
}
function setMode(next){
 if(next==="case"&&!caseStudy)return;
 mode=next==="case"?"case":"recent";
 updateModeControls();
 if(mode==="case")renderCase();else{
  if(caseLayer)caseLayer.clearLayers();
  refresh();status();
 }
 if(map)requestAnimationFrame(()=>map.invalidateSize(false));
}
function renderList(){
 if(mode==="case"&&caseStudy){
  const list=$("#map-point-list");list.replaceChildren();
  for(const p of caseStudy.records){
   const wrap=document.createElement("div");wrap.setAttribute("role","listitem");
   const button=document.createElement("button");button.type="button";button.className="map-list-point";
   button.setAttribute("aria-pressed",String(Boolean(caseSelected&&caseSelected.id===p.id)));
   button.textContent=p.satellite+" · "+time(p.time_utc)+" · "+num(p.latitude,5)+", "+num(p.longitude,5);
   button.addEventListener("click",()=>selectCase(p,true));wrap.append(button);list.append(wrap);
  }
  $("#map-list-range").textContent=caseStudy.records.length+" "+t("caseCount");
  $("#map-list-prev").hidden=true;$("#map-list-next").hidden=true;return;
 }
 $("#map-list-prev").hidden=false;$("#map-list-next").hidden=false;
 if(!state)return;
 const visible=D.filter(state.points,filter);
 const size=8,pages=Math.max(1,Math.ceil(visible.length/size));
 if(page>=pages)page=0;
 const subset=visible.slice(page*size,(page+1)*size);
 const list=$("#map-point-list");list.replaceChildren();
 for(const p of subset){
  const wrap=document.createElement("div");wrap.setAttribute("role","listitem");
  const button=document.createElement("button");button.type="button";button.className="map-list-point";
  button.setAttribute("aria-pressed",String(Boolean(selected&&selected.id===p.id)));
  button.textContent=(p.sensor==="NOAA20"?"NOAA-20":"NOAA-21")+" · "+time(p.observed)+" · "+num(p.lat,4)+", "+num(p.lon,4);
  button.addEventListener("click",()=>selectPoint(p,true));
  wrap.append(button);list.append(wrap);
 }
 $("#map-list-range").textContent=visible.length?(page*size+1)+"–"+(page*size+subset.length)+" "+t("listRange")+" "+visible.length:"0";
 $("#map-list-prev").disabled=page===0;
 $("#map-list-next").disabled=page>=pages-1;
}
function refresh(){
 if(mode==="case"){renderCase();return;}
 updateModeControls();
 if(!state)return;
 const visible=D.filter(state.points,filter);
 for(const b of document.querySelectorAll("[data-map-filter]")){
  b.textContent=b.dataset.mapFilter==="all"?t("all"):b.dataset.mapFilter==="NOAA20"?"NOAA-20":"NOAA-21";
  b.setAttribute("aria-pressed",String(b.dataset.mapFilter===filter));
 }
 $("#map-count").textContent=num(visible.length)+" "+t("loaded");
 const no=visible.length===0;
 $("#map-no-data").hidden=!no;
 $("#map-no-data").textContent=state.points.length?t("noMatch"):t("noPoint");
 if(selected&&!visible.some(p=>p.id===selected.id))selected=null;
 detail(selected);
 renderList();
 if(!map||!layer)return;
 markerRefs.clear();
 layer.clearLayers();
 const bounds=[];
 for(const p of visible){
  const color=p.sensor==="NOAA20"?"sensor20":"sensor21";
  const icon=L.divIcon({className:"map-pixel "+color,html:"<span></span>",iconSize:[18,18],iconAnchor:[9,9]});
  const m=L.marker([p.lat,p.lon],{icon:icon,keyboard:true,title:p.sensor+" · "+time(p.observed),alt:p.sensor+" · "+time(p.observed)});
  m.on("click",()=>selectPoint(p,false));
  markerRefs.set(p.id,m);
  layer.addLayer(m);bounds.push([p.lat,p.lon]);
 }
 if(firstView&&bounds.length){map.fitBounds(L.latLngBounds(bounds).pad(0.12),{maxZoom:7,animate:false});firstView=false;}
}
function translate(){
 for(const el of document.querySelectorAll("[data-map-t]"))el.textContent=t(el.dataset.mapT);
 updateModeControls();
 $("#fire-map").setAttribute("aria-label",t("heading"));
 $("#map-cluster-hint").textContent=t(canCluster?"clusterNote":"clusterFail");
 if(mode==="case"){renderCase();}else if(state){status();refresh();}else{detail(null);}
 if(map)requestAnimationFrame(()=>map.invalidateSize(false));
}
function init(){
 if(!window.L||!L.map){
  $("#map-status").textContent=t("libError");
  $("#fire-map").classList.add("map-missing");
  return;
 }
 map=L.map("fire-map",{scrollWheelZoom:false,maxZoom:15,minZoom:3,zoomControl:true}).setView([-4.3,-63.2],6);
 const tiles=L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png",{attribution:'&copy; <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener noreferrer">OpenStreetMap contributors</a>',maxZoom:19});
 tiles.on("tileerror",()=>{if(++tileErrors===5)$("#map-tile-warning").textContent=t("tileError");});
 tiles.addTo(map);
 canCluster=typeof L.markerClusterGroup==="function";
 layer=canCluster?L.markerClusterGroup({
  maxClusterRadius:45,showCoverageOnHover:false,spiderfyOnMaxZoom:true,
  iconCreateFunction:g=>L.divIcon({className:"map-group",html:"<span>"+g.getChildCount()+"</span>",iconSize:[42,42],iconAnchor:[21,21]})
 }):L.layerGroup();
 layer.addTo(map);
 caseLayer=L.layerGroup().addTo(map);
 window.addEventListener("resize",()=>map.invalidateSize(false));
 document.querySelector('[data-view="agora"]')?.addEventListener("click",()=>requestAnimationFrame(()=>map.invalidateSize(false)));
}
document.addEventListener("firelens:language",e=>{lang=e.detail==="pt-BR"?"pt-BR":"en";translate();});
document.addEventListener("firelens:recent-data",e=>{state=D.derive(e.detail);status();refresh();});
document.addEventListener("firelens:case-data",e=>{
 const x=e.detail;
 if(x&&x.status==="historical_case_not_live"&&Array.isArray(x.records)&&x.records.length===3&&x.analysis?.identity_confirmed===false){
  caseStudy=x;$("#map-show-case").disabled=false;
 }else{
  caseStudy=null;$("#map-show-case").disabled=true;$("#map-show-case").title=t("caseNotReady");
 }
 updateModeControls();
});
$("#map-show-case").addEventListener("click",()=>setMode("case"));
$("#map-show-recent").addEventListener("click",()=>setMode("recent"));

for(const b of document.querySelectorAll("[data-map-filter]"))b.addEventListener("click",()=>{filter=b.dataset.mapFilter;selected=null;page=0;refresh();});
$("#map-list-prev").addEventListener("click",()=>{if(page>0){page--;renderList();}});
$("#map-list-next").addEventListener("click",()=>{if(state&&D.filter(state.points,filter).length>(page+1)*8){page++;renderList();}});
init();translate();
})();