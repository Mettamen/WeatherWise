import { $, element, text } from './format.js';
import { getFoodIdeas, getNearby, isMock } from './api.js';
let generation=0;
export function clearNearby() { generation++; $('#nearby-list').replaceChildren(); text('#nearby-status','Enable location or choose live home-city mode to find nearby places.'); }
export async function renderFood(coords) {
  const revision=++generation;
  $('#meal-list').replaceChildren(); $('#nearby-list').replaceChildren();
  text('#meal-note','Loading meal ideas…');
  text('#nearby-status',coords?'Finding public food-place listings…':'Enable location or choose live home-city mode to find nearby places.');
  if(isMock) {text('#meal-note','Food lookup is available in the integrated app, not the fixed mock.');return;}
  const ideasTask=getFoodIdeas().then(result=>{
    if(revision!==generation)return;
    text('#meal-note',result.note);
    result.ideas.forEach(idea=>{
      const card=element('article','meal-card');card.append(element('h3','',idea.name),element('p','',idea.ingredients),element('small','',idea.note));$('#meal-list').append(card);
    });
  }).catch(()=>{if(revision===generation)text('#meal-note','Meal ideas unavailable. Please retry.');});
  const nearbyTask=coords?getNearby(coords).then(result=>{
    if(revision!==generation)return;
    text('#nearby-status',result.message+(result.status==='available'&&!result.places.length?' No named places were returned within 3 km.':''));
    result.places.forEach(place=>{
      const card=element('article','place-card'); const link=element('a','',place.name);
      if(/^https:\/\/www\.openstreetmap\.org\/(node|way|relation)\/\d+$/.test(place.url)) {link.href=place.url;link.target='_blank';link.rel='noopener noreferrer';}
      card.append(link,element('span','distance',`${place.distance_km} km`),element('p','',place.cuisine),element('small','',`Allergens: ${place.allergen_status}. Opening: ${place.opening_status}.`)); $('#nearby-list').append(card);
    });
  }).catch(()=>{if(revision===generation)text('#nearby-status','Nearby places are unavailable. No venue has been marked allergy-safe.');}):Promise.resolve();
  await Promise.all([ideasTask,nearbyTask]);
}
