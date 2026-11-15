'use strict';
// FireLens interface translations (human-reviewed EN/PT-BR scientific wording).
const TRANSLATIONS = {"brand.subtitle":["DOIS TRADUTORES · STACK MANAUARA","TWO TRANSLATORS · STACK MANAUARA"],"top.science":["CIÊNCIA DE DADOS DA TERRA","EARTH DATA SCIENCE"],"hero.eyebrow":["UMA MESMA PAISAGEM. DIFERENTES OLHARES.","ONE LANDSCAPE. DIFFERENT OBSERVATIONS."],"hero.first":["Os satélites veem o fogo.","Satellites detect thermal anomalies."],"hero.second":["Nós traduzimos os dados.","We translate the data."],"hero.intro":["Sensores distintos não medem a atividade do fogo da mesma forma. Compare as observações, explore as evidências e compreenda os limites — sem confundir detecção com incêndio.","Different sensors observe fire activity differently. Compare observations, explore the evidence, and understand the limits — without confusing a detection with a confirmed fire."],"nav.recent":["Observações recentes","Recent observations"],"nav.science":["Tradutor científico","Scientific translator"],"nav.calendar":["Calendário histórico","Historical calendar"],"recent.kicker":["01 / CAMADA RECENTE","01 / RECENT DATA"],"recent.title":["O que está sendo observado?","What are the satellites observing?"],"recent.subtitle":["Registros de pixels com anomalia térmica identificados por satélites. Não são eventos de incêndio confirmados.","Satellite-detected pixels with thermal anomalies. These are not confirmed individual fire events."],"recent.loading":["● Verificando fonte","● Checking source"],"recent.stat.count":["Detecções elegíveis · 48h","Eligible detections · 48h"],"recent.stat.qualifier":["NOAA-20 + NOAA-21 · confiança nominal/alta","NOAA-20 + NOAA-21 · normal/high confidence"],"recent.stat.update":["Última captura bem-sucedida","Last successful data retrieval"],"recent.stat.updatefoot":["Horário da atualização do sistema","Time of the latest successful query"],"recent.stat.obs":["Última observação disponível","Most recent observation"],"recent.stat.obsfoot":["Horário da detecção pelo satélite","Satellite observation time"],"recent.alert.loading":["Carregando estado da ingestão...","Loading retrieval status..."],"recent.chart.title":["Distribuição por satélite","Breakdown by satellite"],"recent.chart.raw":["CONTAGENS BRUTAS","ORIGINAL COUNTS"],"recent.chart.empty":["Nenhum dado NRT validado disponível ainda.","No verified NRT detections available yet."],"science.human.label":["TRADUTOR HUMANO","HUMAN TRANSLATOR"],"human.label":["TRADUTOR HUMANO / EM LINGUAGEM SIMPLES","HUMAN TRANSLATOR / IN PLAIN LANGUAGE"],"recent.human.title":["O que esses números realmente dizem?","What do these numbers actually mean?"],"recent.human.loading":["Estamos verificando as observações recentes. Um zero na tela não comprova que não houve fogo: nuvens, órbitas e intervalos de aquisição influenciam o que é observado.","We are checking recent observations. A zero on screen does not prove there was no fire: clouds, satellite orbits, and observation timing affect what is detected."],"recent.human.note":["Atualizações automáticas consultam a fonte periodicamente; isso não significa uma nova passagem de satélite a cada hora.","Scheduled retrievals query the source periodically. This does not mean there is a new satellite overpass every hour."],"science.kicker":["02 / EVIDÊNCIA CIENTÍFICA","02 / SCIENTIFIC EVIDENCE"],"science.title":["Dois sensores. Uma escala comparável.","Two sensors. A tested count-scale comparison."],"science.subtitle":["Validamos uma transformação estatística simples para aproximar contagens VIIRS das contagens observadas pelo MODIS Aqua em regiões-piloto.","We tested a simple statistical transformation that brings VIIRS counts closer to MODIS Aqua counts in limited pilot regions."],"science.badge":["● VAL-TRAD-02 / TESTES HISTÓRICOS","● VAL-TRAD-02 / HISTORICAL TESTS"],"science.step1":["1 / OBSERVAR","1 / OBSERVE"],"science.step1.foot":["Contagens originais de pixels","Original pixel-detection counts"],"science.step2":["2 / AJUSTAR","2 / SCALE"],"science.step2.name":["Fator global diurno","Global daytime factor"],"science.step2.foot":["Calculado só com anos de treino","Fitted using training years only"],"science.step3":["3 / COMPARAR","3 / COMPARE"],"science.step3.name":["Escala MODIS Aqua","MODIS Aqua count scale"],"science.step3.foot":["Referência observacional, não verdade do fogo","Observation reference, not fire ground truth"],"science.chart.title":["Quanto o método errou em testes posteriores?","How did the method perform on held-out years?"],"science.chart.note":["WAPE (%) · MENOR É MELHOR","WAPE (%) · LOWER IS BETTER"],"science.chart.desc":["WAPE avalia a diferença na soma de erros absolutos por célula de 1° × mês, dividida pela soma das contagens MODIS. Não é taxa de erro em incêndios reais.","WAPE is the sum of absolute errors across 1° × monthly cells, divided by the sum of MODIS counts. It does not measure error against actual fire events."],"science.chart.loading":["Carregando os resultados verificados...","Loading verified results..."],"science.chart.global":["Global diurno","Global daytime"],"science.chart.seasonal":["Sazonal regularizado","Regularized seasonal"],"science.label":["TRADUTOR CIENTÍFICO","SCIENTIFIC TRANSLATOR"],"science.what.title":["O que foi demonstrado","What was demonstrated"],"science.what.body":["Nos quatro testes diurnos de 2023/2024, o fator global teve desempenho competitivo; o método sazonal não foi consistentemente superior.","Across four daytime tests in 2023 and 2024, the global factor was competitive; the seasonal method was not consistently better."],"science.what.note":["Recortes A/B experimentais; 2022–2024; MODIS Aqua e NOAA-20. A transformação não foi validada para NOAA-21, incêndios físicos nem todo o Amazonas.","Experimental regions A/B; 2022–2024; MODIS Aqua and NOAA-20. The transformation is not validated for NOAA-21, physical fire events, or all of Amazonas."],"science.human.title":["Uma comparação justa","A fair comparison"],"science.human.body":["Imagine duas câmeras com sensibilidades diferentes: contar o que cada uma enxerga pode produzir números muito distintos. O ajuste tenta tornar contagens observadas mais comparáveis — não consegue mostrar o fogo que nenhum sensor detectou.","Imagine two cameras with different sensitivities: each can report a different number of detections. Scaling makes observed counts more comparable; it cannot reveal fire that neither sensor detected."],"science.human.note":["Nuvens, órbitas, resolução e horário de passagem ainda importam.","Clouds, orbit timing, spatial resolution, and observation opportunities still matter."],"calendar.kicker":["03 / EXPLORAR O TEMPO","03 / EXPLORE OVER TIME"],"calendar.title":["Um calendário de observações.","A calendar of observations."],"calendar.subtitle":["Padrões mensais de detecções registradas, com séries históricas originais e ajuste quando validado.","Explore monthly detection patterns, original historical counts, and tested count-scale adjustments."],"calendar.select.label":["REGIÃO EXPERIMENTAL","EXPERIMENTAL REGION"],"calendar.region.a":["Recorte A","Region A"],"calendar.region.b":["Recorte B","Region B"],"calendar.panel.title":["Atividade do fogo · 2022–2024","Detected fire activity · 2022–2024"],"calendar.panel.note":["MODIS AQUA / CONTAGEM MENSAL","MODIS AQUA / MONTHLY COUNTS"],"calendar.loading":["As séries mensais ainda não foram geradas. Os testes científicos já estão disponíveis na seção 02.","Monthly series have not been loaded yet. Scientific test results are available in section 02."],"calendar.legend.low":["MENOS","FEWER"],"calendar.legend.high":["MAIS","MORE"],"calendar.legend.note":["Observações locais solares · Dezembro pode estar incompleto","Local solar months · December may be incomplete"],"calendar.detail.default":["Selecione um mês com dados verificados para ver o comparativo.","Select a verified month to see the sensor comparison."],"footer.source":["Fonte NASA FIRMS ↗","NASA FIRMS data source ↗"],"footer.disclaimer":["Projeto independente · sem endosso da NASA","Independent project · not endorsed by NASA"],"footer.brand":["FIRELENS · DOIS TRADUTORES","FIRELENS · TWO TRANSLATORS"],"meta.description":["FireLens — Dois Tradutores: comparabilidade histórica MODIS/VIIRS e detecções recentes NOAA-20/NOAA-21 NASA FIRMS para o Amazonas. NASA Space Apps 2026.","FireLens — Two Translators: MODIS/VIIRS historical comparisons and recent NOAA-20/NOAA-21 NASA FIRMS detections for Amazonas. NASA Space Apps 2026."],"meta.title":["FireLens · Dois Tradutores | Stack Manauara","FireLens · Two Translators | Stack Manauara"],"dynamic.notavailable":["Não disponível","Not available"],"dynamic.invalid":["Inválido","Invalid"],"dynamic.status.unavailable":["● Dados não disponíveis","● Data unavailable"],"dynamic.status.stale":["● Atualização desatualizada","● Retrieval outdated"],"dynamic.status.ok":["● Fonte consultada","● Source retrieved"],"dynamic.alert.stale":["A última consulta bem-sucedida ocorreu há mais de 4 horas.","The last successful retrieval was over 4 hours ago."],"dynamic.alert.obsold":["A observação mais recente retornada tem mais de 12 horas; isso pode refletir a passagem do satélite e a latência da fonte.","The most recent observation is over 12 hours old; satellite overpass timing and source latency may explain the gap."],"dynamic.alert.ok":["Dados NASA FIRMS consultados; contagens de pixels, não incêndios individuais.","NASA FIRMS data retrieved. These are pixel detections, not individual confirmed fires."],"dynamic.alert.fail":["Não há captura NRT validada.","No verified recent-data snapshot is available."],"dynamic.alert.saved":["Falha em um ou mais sensores; exibindo última captura anterior, se disponível.","One or more sensors failed; the last successful snapshot is retained, if available."],"dynamic.alert.missing":["Não existe atualização NRT bem-sucedida registrada.","No successful recent-data retrieval has been recorded."],"dynamic.alert.zero":["Nenhuma detecção elegível foi retornada na janela consultada; isso não comprova ausência de fogo.","No eligible detections were returned for this window. This does not prove that no fire occurred."],"dynamic.sensor.no":["Sem contagens atuais verificadas. Não confunda indisponibilidade com zero ocorrências.","No verified current counts. Do not confuse unavailable data with zero fire activity."],"dynamic.sensor.failed":["falha","failed"],"dynamic.human.fail":["A última consulta NRT não está disponível. Se houver captura anterior, ela não representa dados atualizados. As validações científicas históricas continuam disponíveis no Tradutor científico; isso não comprova ausência de fogo.","The latest NRT retrieval is unavailable. Any retained snapshot is not a fresh observation. Historical scientific results remain available, and missing data does not prove absence of fire."],"dynamic.human.first":["As","The"],"dynamic.chart.region":["Recorte","Region"],"dynamic.chart.seasonal":["Sazonal","Seasonal"],"dynamic.chart.global":["Global","Global"],"dynamic.calendar.pending":["As séries mensais ainda não foram geradas dos CSVs NASA. Nenhuma contagem foi inventada para preencher o calendário.","Monthly series have not yet been generated from NASA CSVs. No values have been invented for the calendar."],"dynamic.calendar.incomplete":["MÊS INCOMPLETO","INCOMPLETE MONTH"],"dynamic.calendar.obs":["detecções MODIS","MODIS detections"],"dynamic.calendar.noobs":["Sem observações verificadas","No verified observations"],"dynamic.calendar.nottrained":["não calculada (período de treino)","not calculated (training period)"],"dynamic.calendar.available":["Mês disponível.","Month available."],"dynamic.calendar.caveat":["Dezembro potencialmente incompleto: faltam observações UTC do ano seguinte","December may be incomplete: observations from the following UTC year were not included"],"dynamic.calendar.vscale":["VIIRS na escala MODIS","VIIRS on MODIS count scale"],"dynamic.calendar.pixels":["Valores em pixels detectados, não incêndios.","Values represent detected pixels, not individual fires."],"dynamic.calendar.modis":["MODIS Aqua","MODIS Aqua"],"dynamic.calendar.viirs":["NOAA-20","NOAA-20"],"dynamic.validation.unavailable":["Validação histórica não carregada.","Historical validation could not be loaded."],"dynamic.recent.unavailable":["Arquivo de dados recentes indisponível.","Recent-data file is unavailable."],"nav.aria":["Seções","Sections"],"recent.aria":["Observações recentes","Recent observations"],"science.aria":["Tradutor científico","Scientific translator"],"calendar.aria":["Calendário histórico","Historical calendar"],"language.aria":["Idioma / Language","Language / Idioma"],"demo.link":["Ver demonstração","View project demo"]};
Object.assign(TRANSLATIONS,{
 "nav.recent":["Mapa","Map"],"nav.calendar":["Histórico","History"],"nav.science":["Entenda os dados","Understand the data"],
 "hero.eyebrow":["ENTENDA O QUE OS SATÉLITES OBSERVAM.","EXPLORE WHAT THE SATELLITES OBSERVE."],
 "hero.first":["Observações reais do Amazonas.","Real observations from Amazonas."],
 "hero.second":["Dados claros, sem exageros.","Clear data, careful interpretation."],
 "hero.intro":["Explore o mapa, selecione um sinal térmico e entenda as evidências. Uma detecção não confirma um incêndio.","Explore the map, select a thermal signal, and understand the evidence. A detection is not a confirmed fire."],
 "recent.kicker":["01 / MAPA","01 / MAP"],
 "recent.title":["Explore as detecções térmicas no mapa","Explore thermal detections on the map"],
 "recent.subtitle":["Selecione um ponto e veja o que um satélite realmente observou. Os pontos não são incêndios individuais confirmados.","Select a point to understand what a satellite observed. Dots are not confirmed individual fires."],
 "calendar.kicker":["02 / HISTÓRICO","02 / HISTORY"],
 "calendar.title":["Histórico em duas regiões experimentais","History in two experimental regions"],
 "calendar.subtitle":["2022–2024 · regiões-piloto A/B, não um histórico municipal completo do Amazonas. Selecione um mês para comparar observações.","2022–2024 · pilot regions A/B, not a municipality-by-municipality history of Amazonas. Select a month to compare observations."],
 "science.kicker":["03 / ENTENDA OS DADOS","03 / UNDERSTAND THE DATA"],
 "science.title":["O que os satélites realmente medem","Understand what the satellites actually measure"],
 "science.subtitle":["Uma explicação simples, com métodos e incertezas disponíveis quando você quiser aprofundar.","One clear explanation, with methods and uncertainty available when you want them."],
 "science.aria":["Entenda os dados","Understand the data"],
 "ux.recentDetails":["Mais informações · contagens e horários de consulta","More information · counts and retrieval times"],
 "ux.scienceDetails":["Explorar os métodos, testes históricos e fontes","Explore the methods, historical tests and source data"],
 "ux.about.title":["Um satélite observa um sinal térmico — não um incêndio confirmado.","A satellite sees a thermal signal — not a confirmed fire."],
 "ux.about.simple":["MODIS e VIIRS observam a paisagem com pixels de tamanhos diferentes e em horários distintos. Dois sinais próximos podem estar relacionados, mas isso não prova um incêndio único.","MODIS and VIIRS see the landscape with different pixel sizes and at different times. Two nearby signals may be related, but this does not prove a single fire."],
 "ux.about.compare":["A análise histórica ajusta estatisticamente contagens nas regiões-piloto A/B. É diferente do caso real de novembro de 2026 da Visão da Águia.","The historical comparison statistically adjusts counts in pilot regions A/B. This differs from the November 2026 observation-level Eagle's View case."],
 "ux.about.wape":["Em uma análise separada do Amazonas, o erro WAPE em anos independentes piorou de 23,11% em 2024 para 50,73% em 2025. O fator global não é uma correção física universal.","In a separate Amazonas study, held-out WAPE worsened from 23.11% in 2024 to 50.73% in 2025. The global factor is not a universal physical correction."],
 "ux.about.scienceLink":["Ler evidências científicas e limitações ↗","Read the scientific evidence and its limitations ↗"]
});
const q = sel => document.querySelector(sel);
let language = 'en', recentData=null, validationData=null, historyData=null, selectedMonth=null;
function tr(key){return TRANSLATIONS[key]?.[language==='pt-BR'?0:1] || key;}
function num(n,opts={}){return new Intl.NumberFormat(language,opts).format(n);}
function fmtDate(value){
 if(!value)return tr('dynamic.notavailable');
 const d=new Date(value);
 if(!Number.isFinite(d.valueOf()))return tr('dynamic.invalid');
 return new Intl.DateTimeFormat(language,{dateStyle:'short',timeStyle:'short',timeZone:'America/Manaus'}).format(d)+' AMT';
}
function safeStoredLanguage(){try{return localStorage.getItem('firelens-language')}catch(_){return null}}
function storeLanguage(l){try{localStorage.setItem('firelens-language',l)}catch(_){}}
function chooseInitialLanguage(){
 const fromUrl=new URLSearchParams(location.search).get('lang');
 if(fromUrl==='pt-BR'||fromUrl==='en')return fromUrl;
 const stored=safeStoredLanguage();return stored==='pt-BR'||stored==='en'?stored:'en';
}
function setLanguage(next, save=true){
 language=next==='pt-BR'?'pt-BR':'en';
 document.documentElement.lang=language;
 for(const el of document.querySelectorAll('[data-i18n]'))el.textContent=tr(el.dataset.i18n);
 for(const el of document.querySelectorAll('[data-i18n-aria]'))el.setAttribute('aria-label',tr(el.dataset.i18nAria));
 for(const btn of document.querySelectorAll('[data-language]'))btn.setAttribute('aria-pressed',String(btn.dataset.language===language));
 document.title=tr('meta.title');
 const meta=document.querySelector('meta[name="description"]');if(meta)meta.content=tr('meta.description');
 if(save){
  storeLanguage(language);
  try{const url=new URL(location.href);url.searchParams.set('lang',language);history.replaceState(null,'',url.toString());}catch(_){}
 }
 renderRecent();renderValidation();renderCalendar();
 document.dispatchEvent(new CustomEvent('firelens:language',{detail:language}));
}
function tabs(){
 for(const tab of document.querySelectorAll('.tabs button'))tab.addEventListener('click',()=>{
  for(const t of document.querySelectorAll('.tabs button'))t.setAttribute('aria-selected',String(t===tab));
  for(const sec of document.querySelectorAll('.page-section'))sec.classList.toggle('hidden',sec.id!==tab.dataset.view);
 });
}
async function getJSON(url){const r=await fetch(url,{cache:'no-store'});if(!r.ok)throw Error('Unavailable JSON');return await r.json();}
function renderRecent(){
 if(!recentData)return;
 const d=recentData,active=d.status==='ok'&&Boolean(d.last_success_utc);
 const queried=Date.parse(d.last_success_utc||''),observed=Date.parse(d.last_observation_utc||'');
 const stale=active&&Number.isFinite(queried)&&(Date.now()-queried>4*3600000);
 const oldObs=active&&Number.isFinite(observed)&&(Date.now()-observed>12*3600000);
 const pill=q('#status-pill');
 pill.className='pill '+(active&&!stale?'verified':'error');
 pill.textContent=tr(!active?'dynamic.status.unavailable':stale?'dynamic.status.stale':'dynamic.status.ok');
 q('#recent-count').textContent=active?num(d.count??d.detections?.length??0):'—';
 q('#last-success').textContent=fmtDate(d.last_success_utc);
 q('#last-obs').textContent=fmtDate(d.last_observation_utc);
 const alerts=[];
 // Raw server alerts are Portuguese in JSON; normalize known cases rather than displaying mixed-language copy.
 if(d.status!=='ok'){
  if(d.fallback_snapshot)alerts.push(tr('dynamic.alert.saved'));
  else alerts.push(tr('dynamic.alert.fail'));
 }
 if(d.status==='ok'&&!d.detections?.length)alerts.push(tr('dynamic.alert.zero'));
 if(stale)alerts.push(tr('dynamic.alert.stale'));
 if(oldObs)alerts.push(tr('dynamic.alert.obsold'));
 q('#recent-alert').textContent=alerts.join(' ')||tr(active?'dynamic.alert.ok':'dynamic.alert.fail');
 const sources=Object.entries(d.sensors||{});
 if(!active){
  const empty=document.createElement('div');empty.className='empty';empty.textContent=tr('dynamic.sensor.no');
  q('#sensors-graph').replaceChildren(empty);
 }else{
  const max=Math.max(1,...sources.map(([_,x])=>x.summary?.detections||0));
  q('#sensors-graph').replaceChildren(...sources.map(([sensor,x])=>{
   const v=x.summary?.detections||0,e=document.createElement('div');e.className='sensor-row';
   const h=document.createElement('div');h.className='sensor-label';
   const title=document.createElement('span');title.textContent=sensor.replace('VIIRS_','').replace('_NRT','');
   const count=document.createElement('strong');count.textContent=x.status==='ok'?num(v):tr('dynamic.sensor.failed');
   h.append(title,count);
   const track=document.createElement('div');track.className='track';
   const bar=document.createElement('span');bar.style.width=(100*v/max)+'%';track.append(bar);e.append(h,track);return e;
  }));
 }
 const n=num(d.count??d.detections?.length??0);
 q('#human-nrt').textContent=active
  ? language==='en'
   ? `The ${n} eligible detections in this queried window are observed pixels, not individual fires. The latest returned observation is from ${fmtDate(d.last_observation_utc)}. No new records does not prove that no fire occurred.`
   : `As ${n} detecções elegíveis na janela consultada são pixels observados pelos sensores, não incêndios individuais. A última detecção retornada é de ${fmtDate(d.last_observation_utc)}. A ausência de novos registros não prova ausência de fogo.`
  :tr('dynamic.human.fail');
}
function renderValidation(){
 if(!validationData)return;
 const items=validationData.daytime_holdouts||[];
 q('#validation-chart').replaceChildren(...items.map(x=>{
  const values=[x.global.WAPE*100,x.regularized.WAPE*100],row=document.createElement('div');row.className='chart-row';
  const name=document.createElement('span');name.className='chart-name';name.textContent=`${tr('dynamic.chart.region')} ${x.region} · ${x.test}`;
  const group=document.createElement('div');group.className='chart-group';
  for(const [i,v] of values.entries()){
   const track=document.createElement('div');track.className='chart-meter'+(i?' alt':'');
   track.title=`${tr(i?'dynamic.chart.seasonal':'dynamic.chart.global')}: ${num(v,{minimumFractionDigits:2,maximumFractionDigits:2})}%`;
   const bar=document.createElement('span');bar.style.width=Math.min(100,v/42*100)+'%';track.append(bar);group.append(track);
  }
  const result=document.createElement('span');result.className='chart-value';result.textContent=num(values[0],{minimumFractionDigits:2,maximumFractionDigits:2})+'%';
  row.append(name,group,result);return row;
 }));
}
const MONTHS={
 en:['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC'],
 'pt-BR':['JAN','FEV','MAR','ABR','MAI','JUN','JUL','AGO','SET','OUT','NOV','DEZ']
};
function detailMonth(x,region){
 if(!x){q('#calendar-detail').textContent=tr('calendar.detail.default');return;}
 const mm=MONTHS[language][x.month-1],scaled=x.viirs_in_modis_scale===null?tr('dynamic.calendar.nottrained'):num(x.viirs_in_modis_scale,{maximumFractionDigits:2});
 const caveat=x.complete_local_solar_month?tr('dynamic.calendar.available'):tr('dynamic.calendar.caveat');
 q('#calendar-detail').textContent=`${mm}/${x.year} · ${tr('dynamic.chart.region')} ${region}: MODIS Aqua ${num(x.modis_aqua)}; NOAA-20 ${num(x.viirs_noaa20)}; ${tr('dynamic.calendar.vscale')} ${scaled}. ${caveat}. ${tr('dynamic.calendar.pixels')}`;
}
function renderCalendar(){
 if(!historyData||historyData.status!=='ready'||!historyData.months?.length){
  const empty=document.createElement('div');empty.className='empty';empty.textContent=tr('dynamic.calendar.pending');q('#calendar').replaceChildren(empty);
  detailMonth(null);return;
 }
 const region=q('#region').value,items=historyData.months.filter(x=>x.region===region);
 const max=Math.max(1,...items.map(x=>x.modis_aqua));
 const wrap=document.createDocumentFragment(),header=document.createElement('div');header.className='month-top';
 header.append(document.createElement('span'));
 for(const s of MONTHS[language]){const n=document.createElement('span');n.textContent=s;header.append(n)}
 wrap.append(header);
 for(const year of [2022,2023,2024]){
  const row=document.createElement('div');row.className='year-row';
  const label=document.createElement('strong');label.className='year-label';label.textContent=year;row.append(label);
  for(let month=1;month<=12;month++){
   const x=items.find(y=>y.year===year&&y.month===month);
   const cell=document.createElement('button');cell.type='button';cell.className='heat-cell'+(x&&!x.complete_local_solar_month?' incomplete':'');
   if(x){
    const intensity=Math.pow(x.modis_aqua/max,.5);
    cell.style.background=`hsl(${164-intensity*140} ${35+intensity*43}% ${17+intensity*35}%)`;
    cell.title=`${MONTHS[language][month-1]}/${year}: ${num(x.modis_aqua)} ${tr('dynamic.calendar.obs')}${!x.complete_local_solar_month?' — '+tr('dynamic.calendar.incomplete'):''}`;
    cell.setAttribute('aria-label',cell.title);
    if(selectedMonth&&selectedMonth.region===region&&selectedMonth.year===year&&selectedMonth.month===month)cell.classList.add('active');
    cell.addEventListener('click',()=>{
     selectedMonth={region,year,month};
     for(const el of q('#calendar').querySelectorAll('.heat-cell'))el.classList.remove('active');
     cell.classList.add('active');detailMonth(x,region);
    });
   }else{cell.disabled=true;cell.title=tr('dynamic.calendar.noobs')}
   row.append(cell);
  }
  wrap.append(row);
 }
 q('#calendar').replaceChildren(wrap);
 const match=selectedMonth&&selectedMonth.region===region?items.find(x=>x.year===selectedMonth.year&&x.month===selectedMonth.month):null;
 detailMonth(match,region);
}
async function start(){
 tabs();
 for(const b of document.querySelectorAll('[data-language]'))b.addEventListener('click',()=>setLanguage(b.dataset.language,true));
 q('#region').addEventListener('change',()=>{selectedMonth=null;renderCalendar()});
 setLanguage(chooseInitialLanguage(),false);
 try{recentData=await getJSON('data/recente.json')}catch(_){recentData={status:'unavailable',last_success_utc:null,alerts:[]}}
 renderRecent();
 document.dispatchEvent(new CustomEvent('firelens:recent-data',{detail:recentData}));
 try{
  const caseData=await getJSON('data/caso_visao_aguia_20261110.json');
  document.dispatchEvent(new CustomEvent('firelens:case-data',{detail:caseData}));
 }catch(_){document.dispatchEvent(new CustomEvent('firelens:case-data',{detail:null}));}
 try{validationData=await getJSON('data/validacao.json')}catch(_){const el=document.createElement('div');el.className='empty';el.textContent=tr('dynamic.validation.unavailable');q('#validation-chart').replaceChildren(el)}
 renderValidation();
 try{historyData=await getJSON('data/historico.json')}catch(_){historyData=null}
 renderCalendar();
}
start();
