import { $, text, time, element } from './format.js';
let hours = [], metric = 'temperature', selectedIndex = 12;
let currentAlerts = [], displayTimezone = 'Asia/Kolkata';
let dismissed = new Set(JSON.parse(sessionStorage.getItem('weatherwise.dismissed') || '[]'));

export function renderDashboard(data, catalog) {
  const { profile, focus_hour: focus, daily_risk: risk } = data;
  const w = focus.weather;
  displayTimezone = data.timezone;
  text('#greeting', `A little foresight, ${profile.display_name}.`);
  text('#intro-subtitle', 'Your weather. Your routine. A more considered day.');
  text('#profile-avatar', profile.display_name.charAt(0).toUpperCase());
  text('#city-label', data.location.city);
  text('#temperature', Math.round(w.temperature_c));
  text('#weather-description', w.rainfall_mm_hr >= 2.5 ? 'Rain in the outlook' : w.temperature_c >= 32 ? 'A warm day ahead' : 'A milder moment');
  text('#feels-like', `Feels like ${(w.apparent_temperature_c ?? w.heat_index_c).toFixed(1)}°C at ${time(w.timestamp)}`);
  text('#humidity', `${Math.round(w.relative_humidity_pct)}%`);
  text('#wind', `${w.wind_kmh.toFixed(1)} km/h`);
  text('#aqi', w.aqi == null ? 'Unavailable' : `${w.aqi} ${data.mode === 'live' ? 'US AQI' : 'AQI'}`);
  text('#rain', `${w.rainfall_mm_hr.toFixed(1)} mm`);
  text('#risk-badge', `${risk.level.toUpperCase()} RISK`);
  $('#risk-badge').dataset.level = risk.level;
  $('.risk-card').dataset.level = risk.level;
  text('#risk-title', risk.level === 'Low' ? 'Keep an eye ahead.' : risk.level === 'Moderate' ? 'A little extra care.' : 'Plan around the peaks.');
  text('#risk-score', Math.round(risk.score));
  $('#risk-progress').value = risk.score;
  text('#risk-explanation', risk.reasons.slice(0, 2).join(' '));
  text('#primary-advice', risk.advice[0]);
  const details = $('#risk-details'); details.replaceChildren();
  const list = element('ul');
  [...risk.reasons, ...risk.advice, ...data.limitations].forEach(item => list.append(element('li', '', item)));
  details.append(list);
  hours = data.hours; renderChart();
  text('#window-caption', `${profile.activity_duration_hours}-hour activities · available ${String(profile.available_from).padStart(2, '0')}:00–${String(profile.available_until).padStart(2, '0')}:00`);
  const windows = $('#time-windows'); windows.replaceChildren();
  data.best_windows.forEach((window, index) => {
    const card = element('div', 'time-window');
    card.dataset.level = window.level;
    card.append(element('div', 'window-rank', index === 0 ? 'LOWEST SCORE' : `OPTION 0${index + 1}`), element('strong', 'window-time', `${time(window.start)}–${time(window.end)}`), element('div', 'window-score', `${window.level} · ${Math.round(window.average_score)}/100`));
    card.title = window.explanation; windows.append(card);
  });
  if (!data.best_windows.length) windows.append(element('p', 'empty-state', 'No complete window fits your availability. Try adjusting your profile.'));
  currentAlerts = data.alerts; renderAlerts();
  const occupation = catalog.occupations.find(o => o.id === profile.occupation_id)?.name || 'Adult';
  text('#profile-summary', `${profile.age} years · ${occupation} · ${profile.condition_ids.length + (profile.infectious_condition_ids?.length || 0)} conditions · ${profile.allergy_ids?.length || 0} allergies`);
}

function renderChart() {
  const chart = $('#hour-chart'); chart.replaceChildren();
  const values = hours.map(h => metric === 'risk' ? h.risk.score : h.weather.temperature_c);
  const max = metric === 'risk' ? 100 : Math.max(...values, 1);
  hours.forEach((hour, index) => {
    const button = element('button', `hour-bar${selectedIndex === index ? ' selected' : ''}`);
    button.type = 'button';
    if (metric === 'risk') button.dataset.level = hour.risk.level;
    button.setAttribute('aria-label', `${time(hour.weather.timestamp)}, ${metric === 'risk' ? 'risk score' : 'temperature'} ${values[index].toFixed(1)}${metric === 'risk' ? ' out of 100' : ' degrees Celsius'}`);
    button.setAttribute('aria-pressed', String(selectedIndex === index));
    const track = element('span', 'bar-track'); track.setAttribute('aria-hidden', 'true');
    track.append(element('span', `bar-fill bar-${Math.max(0, Math.min(10, Math.round(values[index] / max * 10)))}`));
    button.append(element('span', 'hour-value', `${Math.round(values[index])}${metric === 'risk' ? '' : '°'}`), track, element('span', 'hour-time', time(hour.weather.timestamp)));
    button.addEventListener('click', () => { selectedIndex = index; renderChart(); $('#hour-chart').children[index].focus({ preventScroll: true }); }); chart.append(button);
  });
  const h = hours[selectedIndex] || hours[0];
  if (h) text('#hour-detail', `${time(h.weather.timestamp)} · ${h.weather.temperature_c.toFixed(1)}°C · Feels ${h.weather.heat_index_c.toFixed(1)}°C · ${h.risk.level} risk (${h.risk.score}/100)`);
}

function renderAlerts() {
  const visible = currentAlerts.filter(alert => !dismissed.has(alert.id));
  text('#alert-count', visible.length); text('#nav-alert-count', visible.length);
  const list = $('#alert-list'); list.replaceChildren();
  visible.forEach(alert => {
    const row = element('article', 'alert-item');
    row.dataset.level = alert.severity;
    const body = element('div', 'alert-body');
    body.append(element('h3', '', alert.title), element('p', '', alert.message), element('small', '', `${time(alert.window_start)}–${time(alert.window_end)} · ${displayTimezone}`));
    const close = element('button', 'icon-button', '×'); close.setAttribute('aria-label', `Dismiss ${alert.title}`);
    close.addEventListener('click', () => { dismissed.add(alert.id); sessionStorage.setItem('weatherwise.dismissed', JSON.stringify([...dismissed])); renderAlerts(); });
    row.append(element('span', 'alert-symbol', '!'), body, close); list.append(row);
  });
  if (!visible.length) list.append(element('p', 'empty-state', currentAlerts.length ? 'All alerts dismissed for this sample day. You can restore them above.' : 'No configured elevated-risk alerts for this sample day. Check local conditions before going out.'));
}
export function clearDismissed() { dismissed.clear(); sessionStorage.removeItem('weatherwise.dismissed'); renderAlerts(); }
export function bindDashboard() {
  document.querySelectorAll('[data-metric]').forEach(button => button.addEventListener('click', () => {
    metric = button.dataset.metric;
    document.querySelectorAll('[data-metric]').forEach(b => { b.classList.toggle('selected', b === button); b.setAttribute('aria-pressed', String(b === button)); });
    renderChart();
  }));
  $('#restore-alerts').addEventListener('click', clearDismissed);
  $('#risk-details-toggle').addEventListener('click', () => { const hidden = !$('#risk-details').hidden; $('#risk-details').hidden = hidden; $('#risk-details-toggle').setAttribute('aria-expanded', String(!hidden)); });
}
