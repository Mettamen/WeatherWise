/* Only an explicit user click can start browser geolocation. No stored coordinates. */
import { $, text } from './format.js';
let watch = null, current = null, last = 0;
export const trackedCoordinates = () => current;
export function stopTracking() {
  if (watch !== null) navigator.geolocation.clearWatch(watch);
  watch = null; current = null; last = 0;
  text('#location-status', 'Location tracking is off. You can use your chosen home city instead.');
  $('#enable-location').disabled = false; $('#stop-location').hidden = true;
}
export function bindLocation(onChange) {
  $('#enable-location').addEventListener('click', () => {
    if (!navigator.geolocation) { text('#location-status', 'This browser does not support location. Choose a home city.'); return; }
    text('#location-status', 'Waiting for browser permission. You may decline and use a home city.');
    $('#enable-location').disabled = true; $('#stop-location').hidden = false;
    watch = navigator.geolocation.watchPosition(position => {
      const coords = { latitude: Math.round(position.coords.latitude*100)/100, longitude: Math.round(position.coords.longitude*100)/100 };
      const changed = !current || coords.latitude !== current.latitude || coords.longitude !== current.longitude || Date.now()-last > 300000;
      current = coords;
      text('#location-status', `Tracking while this page is open · device accuracy about ${Math.round(position.coords.accuracy)} m · shared coordinates rounded to ~1 km.`);
      if (changed) { last = Date.now(); onChange(coords); }
    }, error => {
      stopTracking();
      text('#location-status', error.code === 1 ? 'Location permission declined. Choose a home city for live weather.' : 'Could not locate this device. Try again or choose a home city.');
    }, { enableHighAccuracy: false, maximumAge: 120000, timeout: 15000 });
  });
  $('#stop-location').addEventListener('click', () => { stopTracking(); onChange(null); });
  window.addEventListener('pagehide', stopTracking);
}
