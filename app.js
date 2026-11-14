'use strict';
const q = sel => document.querySelector(sel);
const moneyless = n => new Intl.NumberFormat('pt-BR').format(n);
const dateText = val => {
  if (!val) return 'Não disponível';
  const d = new Date(val);
  if (Number.isNaN(d.valueOf())) return 'Inválido';
  return new Intl.DateTimeFormat('pt-BR', {dateStyle:'short',timeStyle:'short',timeZone:'America/Manaus'}).format(d)+' AMT';
};
let hist = null;
function tabs(){
  for(const tab of document.querySelectorAll('.tabs button')) tab.addEventListener('click', () => {
    for(const t of document.querySelectorAll('.tabs button')) t.setAttribute('aria-selected',String(t===tab));
    for(const sec of document.querySelectorAll('.page-section')) sec.classList.toggle('hidden',sec.id!==tab.dataset.view);
  });
}
async function getJSON(url){const response=await fetch(url,{cache:'no-store'});if(!response.ok) throw Error('Arquivo indisponível');return await response.json()}
function recent(data){
  const active = data.status === 'ok' && data.last_success_utc;
  const queriedAt = Date.parse(data.last_success_utc || '');
  const observedAt = Date.parse(data.last_observation_utc || '');
  const staleQuery = active && Number.isFinite(queriedAt) && (Date.now() - queriedAt > 4*60*60*1000);
  const oldObservation = active && Number.isFinite(observedAt) && (Date.now() - observedAt > 12*60*60*1000);
  const pill=q('#status-pill');
  pill.className='pill '+(active && !staleQuery ? 'verified' : 'error');
  pill.textContent=!active ? '● Dados não disponíveis' : staleQuery ? '● Atualização desatualizada' : '● Fonte consultada';
  q('#recent-count').textContent=active?moneyless(data.count??data.detections?.length??0):'—';
  q('#last-success').textContent=dateText(data.last_success_utc);
  q('#last-obs').textContent=dateText(data.last_observation_utc);
  const alerts=Array.isArray(data.alerts)?[...data.alerts]:[];
  if (staleQuery) alerts.push('A última consulta bem-sucedida ocorreu há mais de 4 horas.');
  if (oldObservation) alerts.push('A observação mais recente retornada tem mais de 12 horas; isso pode refletir a passagem do satélite e a latência da fonte.');
  q('#recent-alert').textContent=alerts.join(' ')||(active?'Dados NASA FIRMS consultados; contagens de pixels, não incêndios individuais.':'Não há captura NRT validada.');
  let sources = Object.entries(data.sensors||{});
  if(!active){q('#sensors-graph').innerHTML='<div class="empty">Sem contagens atuais verificadas. Não confunda indisponibilidade com zero ocorrências.</div>'}
  else{
    let max=Math.max(1,...sources.map(([_,x])=>x.summary?.detections||0));
    q('#sensors-graph').replaceChildren(...sources.map(([sensor,x])=>{
      const v=x.summary?.detections||0, element=document.createElement('div');element.className='sensor-row';
      const header=document.createElement('div');header.className='sensor-label';
      const title=document.createElement('span');title.textContent=sensor.replace('VIIRS_','').replace('_NRT','');
      const count=document.createElement('strong');count.textContent=x.status==='ok'?moneyless(v):'falha';header.append(title,count);
      const track=document.createElement('div');track.className='track';const bar=document.createElement('span');bar.style.width=(100*v/max)+'%';track.append(bar);element.append(header,track);return element;
    }));
  }
  q('#human-nrt').textContent=active
    ? `As ${moneyless(data.count??data.detections?.length??0)} detecções elegíveis na janela consultada são pixels observados pelos sensores, não incêndios individuais. A última detecção retornada é de ${dateText(data.last_observation_utc)}. A ausência de novos registros não prova ausência de fogo.`
    : 'A última consulta NRT não está disponível. Se houver captura anterior, ela não representa dados atualizados. As validações científicas históricas continuam disponíveis no Tradutor científico; isso não comprova ausência de fogo.';
}
function validation(data){
  let arr=data.daytime_holdouts||[];
  q('#validation-chart').replaceChildren(...arr.map(x=>{
    const v=x.global.WAPE*100, alt=x.regularized.WAPE*100;
    const row=document.createElement('div');row.className='chart-row';
    const name=document.createElement('span');name.className='chart-name';name.textContent=`Recorte ${x.region} · ${x.test}`;
    const group=document.createElement('div');group.className='chart-group';
    for(const [value,secondary] of [[v,false],[alt,true]]){
      const track=document.createElement('div');track.className='chart-meter'+(secondary?' alt':'');
      track.title=`${secondary?'Sazonal':'Global'}: ${value.toFixed(2).replace('.',',')}%`;
      const bar=document.createElement('span');bar.style.width=Math.min(100,value/42*100)+'%';track.append(bar);group.append(track);
    }
    const value=document.createElement('span');value.className='chart-value';value.textContent=v.toFixed(2).replace('.',',')+'%';
    row.append(name,group,value);return row;
  }));
}
const monthNames=['JAN','FEV','MAR','ABR','MAI','JUN','JUL','AGO','SET','OUT','NOV','DEZ'];
function calendar(){
  if (!hist || hist.status!=='ready' || !hist.months?.length){q('#calendar').innerHTML='<div class="empty">As séries mensais ainda não foram geradas dos CSVs NASA. Nenhuma contagem foi inventada para preencher o calendário.</div>';return;}
  const region=q('#region').value;
  const items=hist.months.filter(x=>x.region===region),max=Math.max(1,...items.map(x=>x.modis_aqua));
  const wrap=document.createDocumentFragment(),header=document.createElement('div');header.className='month-top';
  header.append(document.createElement('span'));
  for(const name of monthNames){const node=document.createElement('span');node.textContent=name;header.append(node)}
  wrap.append(header);
  for (const year of [2022,2023,2024]){
    const row=document.createElement('div');row.className='year-row';const label=document.createElement('strong');label.className='year-label';label.textContent=year;row.append(label);
    for(let month=1;month<=12;month++){
      const x=items.find(x=>x.year===year && x.month===month);
      const cell=document.createElement('button');cell.type='button';cell.className='heat-cell'+(x&&!x.complete_local_solar_month?' incomplete':'');
      if(x){const intensity=Math.pow(x.modis_aqua/max,.5);cell.style.background=`hsl(${164-intensity*140} ${35+intensity*43}% ${17+intensity*35}%)`;cell.title=`${monthNames[month-1]}/${year}: ${moneyless(x.modis_aqua)} detecções MODIS${x.caveat?' — MÊS INCOMPLETO':''}`;cell.setAttribute('aria-label',cell.title);cell.addEventListener('click',()=>{
        for(const el of q('#calendar').querySelectorAll('.heat-cell'))el.classList.remove('active');cell.classList.add('active');
        const adjusted=x.viirs_in_modis_scale===null?'não calculada (período de treino)':moneyless(x.viirs_in_modis_scale);
        q('#calendar-detail').textContent=`${monthNames[month-1]}/${year} · Recorte ${region}: MODIS Aqua ${moneyless(x.modis_aqua)}; NOAA-20 ${moneyless(x.viirs_noaa20)}; VIIRS na escala MODIS ${adjusted}. ${x.caveat||'Mês disponível.'} Valores em pixels detectados, não incêndios.`;
      })}
      else{cell.disabled=true;cell.title='Sem observações verificadas'}
      row.append(cell);
    }
    wrap.append(row);
  }
  q('#calendar').replaceChildren(wrap);
}
async function start(){
  tabs();q('#region').addEventListener('change',calendar);
  try{recent(await getJSON('data/recente.json'))}catch(e){recent({status:'unavailable',alerts:['Arquivo de dados recentes indisponível.']})}
  try{validation(await getJSON('data/validacao.json'))}catch(e){q('#validation-chart').innerHTML='<div class="empty">Validação histórica não carregada.</div>'}
  try{hist=await getJSON('data/historico.json')}catch(e){hist=null}
  calendar();
}
start();
