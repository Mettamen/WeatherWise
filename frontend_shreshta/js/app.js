import { $, text, dateLabel, element, setTimezone } from './format.js';
import { ensureSession, getCatalog, getDashboard, getLive, isMock } from './api.js';
import { renderDashboard, bindDashboard } from './dashboard.js';
import { configureProfile, bindProfile, openProfile } from './profile.js';
import { bindLocation, trackedCoordinates, stopTracking } from './location.js';
import { renderFood, clearNearby } from './food.js';
import { renderScene } from './weather-scene.js';
let catalog, currentDate='2026-05-08', profile, loadSequence=0, busy=false;
function coordsForMode(){
  if($('#weather-mode').value!=='live')return null;
  const tracked=trackedCoordinates();if(tracked)return tracked;
  const city=catalog.locations.find(c=>c.location_id===(profile?.home_location_id||'LOC01'));
  return {latitude:city.latitude,longitude:city.longitude};
}
function renderSources(data){
  const live=data.mode==='live';$('#source-panel').hidden=!live;$('#sample-date-label').hidden=live;
  text('#data-mode-badge',live?'LIVE MODEL DATA':'SAMPLE DATA');
  text('#data-notice',live?'Weather is fetched from forecast models; health scores remain illustrative.':'Sample weather is synthetic.');
  text('#weather-time',live?'Current model estimate':'12:00 IST snapshot');
  text('#zone-label',data.timezone);text('#chart-timezone',`Times in ${data.timezone}`);
  text('#weather-source-label',live?`Valid ${data.valid_at.slice(11,16)} · ${data.timezone}`:'Illustrative conditions · not a live forecast');
  text('#risk-period-label',live?'PEAK RISK REMAINING TODAY':'PEAK RISK FOR THIS SAMPLE DAY');
  if(!live)return;
  text('#comparison-status',data.comparison.status);$('#comparison-status').dataset.status=data.comparison.status;
  text('#comparison-message',data.comparison.message);
  const list=$('#source-list');list.replaceChildren();
  data.sources.forEach(source=>{
    const card=element('div','source-card');const link=element('a','',source.name);link.href=source.url;link.target='_blank';link.rel='noopener noreferrer';
    card.append(link,element('strong','',source.status),element('small','',source.temperature_c==null?'':`${source.temperature_c}°C · ${source.valid_at}`));list.append(card);
  });
  text('#source-age',`Retrieved ${new Date(data.fetched_at).toLocaleString()}. ${data.location_note} Models share one delivery provider; agreement is not proof of accuracy. Missing AQI/UV are excluded from risk.`);
}
async function refresh(){
  const sequence=++loadSequence;busy=true;
  $('#error-panel').hidden=true;$('#loading').hidden=false;$('#dashboard').hidden=true;clearNearby();
  try{
    const sample=await getDashboard(currentDate);
    if(sequence!==loadSequence)return false;
    profile=sample.profile;configureProfile(catalog,profile);
    const coords=coordsForMode();const data=coords?await getLive(coords):sample;
    if(sequence!==loadSequence)return false;
    if(coords&&!trackedCoordinates())data.location.city=catalog.locations.find(c=>c.location_id===profile.home_location_id).city;
    setTimezone(data.timezone);renderDashboard(data,catalog);renderScene(data);renderSources(data);
    $('#dashboard').hidden=false;renderFood(coords);return true;
  }catch(error){
    if(sequence!==loadSequence)return false;
    text('#error-message',error.message);$('#error-panel').hidden=false;return false;
  }finally{if(sequence===loadSequence){$('#loading').hidden=true;busy=false;}}
}
async function start(){
  $('#error-panel').hidden=true;$('#loading').hidden=false;
  try{
    await ensureSession();catalog=await getCatalog();
    if(!catalog.dates.includes(currentDate))currentDate=catalog.dates[0];
    const select=$('#sample-date');select.replaceChildren();
    catalog.dates.forEach(date=>{const o=element('option','',dateLabel(date));o.value=date;select.append(o);});select.value=currentDate;
    await refresh();
  }catch(error){text('#error-message',error.message);$('#error-panel').hidden=false;$('#loading').hidden=true;}
}
function scenario(){
  const value=Number($('#pm-slider').value),score=Math.round(value/150*100);
  const level=score>=75?'Severe':score>=50?'High':score>=25?'Moderate':'Low';
  text('#pm-value',`${value} µg/m³`);text('#pm-level',`${level} · ${score}/100`);$('#pm-level').dataset.level=level;
  const baseline=$('#patient-baseline').selectedOptions[0].text;
  text('#scenario-note',`${baseline}: this selector provides context only; it does not estimate individual disease risk. Current manual exposure index: ${score}/100.`);
}
bindDashboard();bindProfile(refresh,()=>{stopTracking();$('#weather-mode').value='sample';});
bindLocation(coords=>{if(!catalog)return;$('#weather-mode').value=coords?'live':'sample';refresh();});
$('#sample-date').addEventListener('change',event=>{currentDate=event.target.value;refresh();});
$('#weather-mode').addEventListener('change',()=>{if($('#weather-mode').value==='sample')stopTracking();refresh();});
$('#refresh-weather').addEventListener('click',()=>{if(!busy)refresh();});
$('#retry').addEventListener('click',start);
$('#pm-slider').addEventListener('input',scenario);$('#patient-baseline').addEventListener('change',scenario);scenario();
document.querySelectorAll('[data-nav]').forEach(button=>button.addEventListener('click',()=>{
  if(button.dataset.nav==='profile'){openProfile();return;}
  document.querySelectorAll('[data-nav]').forEach(b=>{b.classList.toggle('active',b===button);if(b===button)b.setAttribute('aria-current','page');else b.removeAttribute('aria-current');});
  text('#page-label',{overview:'Overview',forecast:'Hourly outlook',alerts:'Your alerts'}[button.dataset.nav]);
  $(`#${button.dataset.nav}`).scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth',block:'start'});
}));
setInterval(()=>{if(!busy&&!document.hidden&&$('#weather-mode').value==='live')refresh();},600000);
if(isMock){text('#mode-label','Frontend mock mode: fixed weather and risk fixtures.');$('#weather-mode').disabled=true;$('#enable-location').disabled=true;}
start();
