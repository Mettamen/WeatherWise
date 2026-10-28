/* Shreshta: all networking lives here. No fetch calls in presentation modules. */
const mock = new URLSearchParams(location.search).get('mock') === '1';
let mockApi;
const key = 'weatherwise.demo.token';
export const isMock = mock;

export class ApiError extends Error {
  constructor(message, status) { super(message); this.status = status; }
}

async function request(path, options = {}) {
  if (mock) {
    mockApi ??= (await import('../mock/mock-api.js')).mockRequest;
    return mockApi(path, options);
  }
  const token = sessionStorage.getItem(key);
  let response;
  try {
    response = await fetch(`/api/v1${path}`, {
      ...options,
      headers: { 'Content-Type': 'application/json', ...(token ? { Authorization: `Bearer ${token}` } : {}), ...options.headers },
      signal: AbortSignal.timeout(25000),
    });
  } catch {
    throw new ApiError('Cannot reach the backend. Start the WeatherWise server, then try again. For frontend-only work, open ?mock=1.', 0);
  }
  if (response.status === 204) return null;
  const payload = await response.json().catch(() => null);
  if (!response.ok) {
    const detail = payload?.detail;
    const message = Array.isArray(detail) ? detail.map(item => item.msg).join('; ') : detail;
    throw new ApiError(message || `Request failed (${response.status}).`, response.status);
  }
  return payload;
}

export async function ensureSession() {
  if (!mock && sessionStorage.getItem(key)) {
    try { await request('/profile'); return; }
    catch (error) { if (error.status !== 401) throw error; sessionStorage.removeItem(key); }
  }
  const session = await request('/sessions', { method: 'POST' });
  if (!mock) sessionStorage.setItem(key, session.token);
}
export const getCatalog = () => request('/catalog');
export const getDashboard = date => request(`/dashboard?date=${encodeURIComponent(date)}`);
export const saveProfile = profile => request('/profile', { method: 'PUT', body: JSON.stringify(profile) });
export const getLive = coords => request('/live', { method: 'POST', body: JSON.stringify(coords) });
export const getFoodIdeas = () => request('/food/ideas');
export const getNearby = coords => request('/food/nearby', { method: 'POST', body: JSON.stringify(coords) });
export async function resetSession() {
  await request('/session', { method: 'DELETE' });
  sessionStorage.removeItem(key);
  await ensureSession();
}
