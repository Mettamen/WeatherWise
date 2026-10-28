/* Shreshta can develop independently: serve frontend_shreshta and open ?mock=1.
 * Fixtures are generated from the shared contract, never from a live service.
 * Profile edits are in memory. Scores intentionally remain fixture values.
 */
let fixture, catalog, profile;
async function initialize() {
  if (fixture) return;
  const results = await Promise.all([fetch('./mock/dashboard.json'), fetch('./mock/catalog.json')]);
  if (results.some(r => !r.ok)) throw new Error('Mock fixtures missing. Run scripts/export_contracts.py once.');
  [fixture, catalog] = await Promise.all(results.map(r => r.json()));
  profile = structuredClone(fixture.profile);
}
export async function mockRequest(path, options = {}) {
  await initialize();
  const method = options.method || 'GET';
  if (path === '/sessions') return { token: 'frontend-mock-only', profile };
  if (path === '/catalog') return { ...catalog, dates: [fixture.date] };
  if (path === '/session' && method === 'DELETE') { profile = structuredClone(fixture.profile); return null; }
  if (path === '/profile' && method === 'PUT') { profile = JSON.parse(options.body); return structuredClone(profile); }
  if (path === '/profile') return structuredClone(profile);
  if (path.startsWith('/dashboard')) {
    const result = structuredClone(fixture); result.profile = structuredClone(profile);
    result.location = catalog.locations.find(c => c.location_id === profile.home_location_id);
    // Availability still filters displayed fixture windows; it does not rescore.
    result.best_windows = result.best_windows.filter(w => Number(w.start.slice(11, 13)) >= profile.available_from && Number(w.end.slice(11, 13)) <= profile.available_until && (new Date(w.end) - new Date(w.start)) / 3600000 === profile.activity_duration_hours);
    return result;
  }
  throw new Error(`Mock endpoint is not implemented: ${method} ${path}`);
}
