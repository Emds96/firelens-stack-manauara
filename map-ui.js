/* MAP-01: interactive, bilingual, point-level NASA FIRMS translator. */
(function(){
"use strict";
const $=s=>document.querySelector(s),D=window.FireLensMapData;
if(!D||!$("#fire-map"))return;
const i18n={
 en:{listTitle:"Select a detection",listPrev:"Previous",listNext:"Next",listRange:"of",heading:"Explore recent satellite detections",explain:"Click a marker to inspect a real NASA FIRMS detection. A point is not a confirmed individual fire or a burned-area polygon.",all:"Both satellites",filter:"Filter satellites",loaded:"visible detections",select:"Select a satellite marker for its scientific and human explanations.",source:"NASA FIRMS Area API",statusOK:"Source retrieved",statusOld:"Outdated snapshot — not current",statusFailed:"Source unavailable — earlier snapshot",statusEmpty:"No available NASA detections",updated:"Latest successful retrieval",observed:"Latest returned observation",stale:"The last retrieval is over four hours old.",previous:"The current retrieval failed; markers, if present, belong to an earlier snapshot.",latency:"A recent retrieval does not imply a recent satellite observation.",border:"The simplified Amazonas boundary has not been verified against the official IBGE geometry.",noPoint:"There are no verified coordinates to display; this does not mean there were no fires.",noMatch:"No detections match the selected satellite.",libError:"Map library unavailable. Other FireLens features remain available.",tileError:"Background tiles could not load; coordinate data remains available.",clusterNote:"Nearby markers are clustered. Zoom in to inspect individual detections.",clusterFail:"Clustering unavailable; individual markers are displayed.",science:"Scientific translator",human:"Human translator",satellite:"Satellite",coords:"Coordinates (lat, lon)",time:"Observation time (Manaus)",confidence:"Reported confidence",daynight:"Day / night",day:"Daytime",night:"Nighttime",normal:"Normal (n)",high:"High (h)",unknown:"Not specified",scienceDesc:"Coordinates indicate a detected pixel, not the size of a fire. NASA FIRMS confidence is a sensor category, not a probability that a fire occurred.",humanIntro:"Satellite",humanObserved:"detected a",humanConfidence:"confidence thermal anomaly during",humanEnding:"at this location and observation time. This is a pixel-level thermal signal, not proof of an individual fire or its burned area.",footer:"Map background: © OpenStreetMap contributors. NASA FIRMS provides observation points, not burned-area shapes."},
 "pt-BR":{listTitle:"Selecione uma detecção",listPrev:"Anterior",listNext:"Próxima",listRange:"de",heading:"Explore as detecções recentes no mapa",explain:"Clique em um marcador para consultar uma detecção real NASA FIRMS. Um ponto não é um incêndio individual confirmado nem um polígono de área queimada.",all:"Ambos os satélites",filter:"Filtrar satélites",loaded:"detecções visíveis",select:"Selecione um marcador para ver as explicações científica e humana.",source:"NASA FIRMS Area API",statusOK:"Fonte consultada",statusOld:"Captura desatualizada — não é atual",statusFailed:"Fonte indisponível — captura anterior",statusEmpty:"Sem detecções NASA disponíveis",updated:"Última consulta bem-sucedida",observed:"Última observação retornada",stale:"A última consulta ocorreu há mais de quatro horas.",previous:"A consulta atual falhou; os marcadores, se presentes, são de uma captura anterior.",latency:"Uma consulta recente não significa uma observação recente do satélite.",border:"O contorno simplificado do Amazonas ainda não foi conferido com a geometria oficial do IBGE.",noPoint:"Não há coordenadas verificadas para exibir; isso não significa ausência de incêndios.",noMatch:"Nenhuma detecção corresponde ao satélite selecionado.",libError:"Biblioteca do mapa indisponível. As outras funções do FireLens continuam acessíveis.",tileError:"Mapa-base não carregou; as coordenadas continuam disponíveis.",clusterNote:"Marcadores próximos são agrupados. Amplie o zoom para explorar os pontos.",clusterFail:"O agrupamento não carregou; os pontos individuais são exibidos.",science:"Tradutor científico",human:"Tradutor humano",satellite:"Satélite",coords:"Coordenadas (lat, lon)",time:"Horário da observação (Manaus)",confidence:"Confiança informada",daynight:"Dia / noite",day:"Diurna",night:"Noturna",normal:"Normal (n)",high:"Alta (h)",unknown:"Não especificado",scienceDesc:"As coordenadas indicam um pixel detectado, não o tamanho do incêndio. A confiança NASA FIRMS é uma categoria do sensor, não uma probabilidade de ter ocorrido incêndio.",humanIntro:"O satélite",humanObserved:"registrou uma anomalia térmica de confiança",humanConfidence:"no período",humanEnding:"neste local e horário. Trata-se de um sinal térmico em um pixel, não uma confirmação de incêndio individual nem de sua área queimada.",footer:"Mapa-base: © colaboradores do OpenStreetMap. NASA FIRMS fornece pontos de observação, não polígonos de área queimada."}
};
let lang="en",filter="all",map=null,layer=null,state=null,selected=null,firstView=true,tileErrors=0,canCluster=false,page=0;
let markerRefs=new Map();
const t=k=>(i18n[lang]||i18n.en)[k]||k;
const num=(n,p=0)=>new Intl.NumberFormat(lang,{minimumFractionDigits:p,maximumFractionDigits:p}).format(n);
function time(x){if(!x||!Number.isFinite(Date.parse(x)))return "—";return new Intl.DateTimeFormat(lang,{dateStyle:"medium",timeStyle:"short",timeZone:"America/Manaus"}).format(new Date(x))+" AMT";}
function status(){
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
function detail(p){
 const out=$("#map-inspector-details");out.replaceChildren();
 if(!p){out.classList.add("map-placeholder");out.textContent=t("select");return;}
 out.classList.remove("map-placeholder");
 const s=document.createElement("h4");s.textContent=t("science");
 const dl=document.createElement("dl");dl.className="map-fields";
 const sensor=p.sensor==="NOAA20"?"NOAA-20":"NOAA-21";
 const conf=p.confidence.toLowerCase()==="h"?t("high"):p.confidence.toLowerCase()==="n"?t("normal"):p.confidence;
 const daytime=p.daynight==="D"?t("day"):p.daynight==="N"?t("night"):t("unknown");
 dl.append(field(t("satellite"),sensor),field(t("coords"),num(p.lat,5)+", "+num(p.lon,5)),field(t("time"),time(p.observed)),field(t("confidence"),conf),field(t("daynight"),daytime),field(t("source"),"NASA FIRMS"));
 const scientific=document.createElement("p");scientific.className="map-science-note";scientific.textContent=t("scienceDesc");
 const h=document.createElement("h4");h.textContent=t("human");
 const human=document.createElement("p");human.className="map-human-note";
 human.textContent=t("humanIntro")+" "+sensor+" "+t("humanObserved")+" "+conf.toLowerCase()+" "+t("humanConfidence")+" "+daytime.toLowerCase()+" "+t("humanEnding");
 out.append(s,dl,scientific,h,human);
}
function selectPoint(p,zoomToPoint){
 selected=p;detail(p);renderList();
 if(zoomToPoint&&map&&markerRefs.has(p.id)){
  const marker=markerRefs.get(p.id);
  if(canCluster&&typeof layer.zoomToShowLayer==="function"){
   layer.zoomToShowLayer(marker,()=>map.panTo(marker.getLatLng(),{animate:false}));
  }else map.setView([p.lat,p.lon],Math.max(9,map.getZoom()),{animate:false});
 }
 $("#map-inspector-details").focus({preventScroll:true});
}
function renderList(){
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
 $("#fire-map").setAttribute("aria-label",t("heading"));
 $("#map-cluster-hint").textContent=t(canCluster?"clusterNote":"clusterFail");
 if(state){status();refresh();}else{detail(null);}
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
 window.addEventListener("resize",()=>map.invalidateSize(false));
 document.querySelector('[data-view="agora"]')?.addEventListener("click",()=>requestAnimationFrame(()=>map.invalidateSize(false)));
}
document.addEventListener("firelens:language",e=>{lang=e.detail==="pt-BR"?"pt-BR":"en";translate();});
document.addEventListener("firelens:recent-data",e=>{state=D.derive(e.detail);status();refresh();});
for(const b of document.querySelectorAll("[data-map-filter]"))b.addEventListener("click",()=>{filter=b.dataset.mapFilter;selected=null;page=0;refresh();});
$("#map-list-prev").addEventListener("click",()=>{if(page>0){page--;renderList();}});
$("#map-list-next").addEventListener("click",()=>{if(state&&D.filter(state.points,filter).length>(page+1)*8){page++;renderList();}});
init();translate();
})();