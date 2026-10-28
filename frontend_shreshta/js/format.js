export const $ = selector => document.querySelector(selector);
export const text = (selector, value) => { $(selector).textContent = value; };
let timezone = 'Asia/Kolkata';
export const setTimezone = zone => { timezone = zone; };
export const time = iso => new Intl.DateTimeFormat('en-GB', { hour: '2-digit', minute: '2-digit', timeZone: timezone }).format(new Date(iso));
export const dateLabel = date => new Intl.DateTimeFormat('en-GB', { day: 'numeric', month: 'short', year: 'numeric', timeZone: 'Asia/Kolkata' }).format(new Date(`${date}T12:00:00+05:30`));
export function element(tag, className, content) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (content !== undefined) node.textContent = content;
  return node;
}
let toastTimer;
export function toast(message) {
  text('#toast', message); $('#toast').hidden = false;
  clearTimeout(toastTimer); toastTimer = setTimeout(() => { $('#toast').hidden = true; }, 4000);
}
