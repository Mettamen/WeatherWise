import { $, text } from './format.js';
export function renderScene(data) {
  const w=data.focus_hour.weather;
  let scene=data.scene;
  if (data.mode!=='live') scene=w.rainfall_mm_hr>.1?'rain':w.wind_kmh>=25?'wind':'sunny';
  const card=$('.weather-card'); card.dataset.scene=scene; card.dataset.night=String(!w.is_day);
  text('#weather-description', {sunny:'Clear skies',partly:'Partly cloudy',cloudy:'Cloudy skies',rain:'Rain in the area',wind:'A windy outlook',night:'Night skies',fog:'Misty conditions',snow:'Snow in the area',storm:'Thunderstorm conditions'}[scene] || 'Weather outlook');
  text('#scene-description',data.mode==='live'?'Animation follows model weather code, cloud cover, wind and day/night; it is not a live camera.':'Illustration follows the selected synthetic conditions.');
}
