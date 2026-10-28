import { $, element, toast } from './format.js';
import { saveProfile, resetSession, isMock } from './api.js';
import { clearDismissed } from './dashboard.js';
let catalog, profile, onSave, selected;
export function configureProfile(nextCatalog, nextProfile) { catalog = nextCatalog; profile = nextProfile; }
function renderSelections() {
  const container=$('#selected-health'); container.replaceChildren();
  const groups=[['condition_ids',catalog.conditions],['infectious_condition_ids',catalog.infectious_conditions||[]],['allergy_ids',catalog.allergies||[]]];
  for(const [field,options] of groups) for(const id of selected[field]) {
    const name=options.find(o=>o.id===id)?.name||id;
    const chip=element('button','health-chip',`${name} ×`);chip.type='button';chip.setAttribute('aria-label',`Remove ${name}`);
    chip.addEventListener('click',()=>{selected[field]=selected[field].filter(v=>v!==id);renderSelections();});container.append(chip);
  }
  if(!container.children.length) container.append(element('p','footnote','No conditions or allergies selected.'));
}
function populate(selectId, groups) {
  const select=$(selectId);select.replaceChildren();const blank=element('option','','Choose to add…');blank.value='';select.append(blank);
  for(const [label,options] of groups) {
    const group=element('optgroup');group.label=label;
    options.forEach(o=>{const option=element('option','',o.name);option.value=o.value||o.id;group.append(option);});select.append(group);
  }
}
export function openProfile() {
  if(!catalog||!profile)return;
  const form=$('#profile-form');
  for(const [field,entries] of [['home_location_id',catalog.locations.map(c=>({id:c.location_id,name:c.city}))],['occupation_id',catalog.occupations]]){
    const select=form.elements[field];select.replaceChildren();entries.forEach(entry=>{const option=element('option','',entry.name);option.value=entry.id;select.append(option);});
  }
  for(const field of ['available_from','available_until']){
    const select=form.elements[field];select.replaceChildren();
    for(let hour=field==='available_from'?0:1;hour<=(field==='available_from'?23:24);hour++){const o=element('option','',`${String(hour).padStart(2,'0')}:00`);o.value=hour;select.append(o);}
  }
  Object.entries(profile).forEach(([key,value])=>{if(form.elements[key])form.elements[key].value=value;});
  selected={condition_ids:[...profile.condition_ids],infectious_condition_ids:[...(profile.infectious_condition_ids||[])],allergy_ids:[...(profile.allergy_ids||[])]};
  populate('#noncomm-select',[
    ['Noncommunicable conditions',catalog.conditions.filter(c=>!['allergy','other'].includes(c.group))],
    ['Other health factors',catalog.conditions.filter(c=>c.group==='other')],
  ]);
  populate('#infectious-select',[['Communicable conditions',catalog.infectious_conditions||[]]]);
  populate('#allergy-select',[
    ['Food allergens',(catalog.allergies||[]).filter(a=>a.group==='food')],
    ['Environmental allergies',(catalog.allergies||[]).filter(a=>a.group==='environmental')],
    ['Allergic conditions',catalog.conditions.filter(c=>c.group==='allergy').map(c=>({...c,value:`condition:${c.id}`}))],
  ]);
  renderSelections();$('#profile-error').textContent='';$('#profile-dialog').showModal();
}
export function bindProfile(saveCallback, resetCallback=()=>{}) {
  onSave=saveCallback;
  ['#edit-profile','#profile-avatar','#update-profile','#food-profile'].forEach(selector=>$(selector).addEventListener('click',openProfile));
  $('#close-profile').addEventListener('click',()=>$('#profile-dialog').close());
  for(const [selector,field] of [['#noncomm-select','condition_ids'],['#infectious-select','infectious_condition_ids'],['#allergy-select','allergy_ids']]){
    $(selector).addEventListener('change',event=>{
      const value=event.target.value;if(!value)return;
      const actualField=value.startsWith('condition:')?'condition_ids':field;const id=value.replace('condition:','');
      if(!selected[actualField].includes(id))selected[actualField].push(id);
      event.target.value='';renderSelections();
    });
  }
  $('#profile-form').addEventListener('submit',async event=>{
    event.preventDefault();const data=new FormData(event.currentTarget);
    const update={display_name:data.get('display_name').trim(),age:Number(data.get('age')),home_location_id:data.get('home_location_id'),occupation_id:data.get('occupation_id'),...selected,
      other_allergy:data.get('other_allergy').trim(),baseline:profile.baseline||'standard',available_from:Number(data.get('available_from')),available_until:Number(data.get('available_until')),activity_duration_hours:Number(data.get('activity_duration_hours'))};
    if(!update.display_name||update.available_until-update.available_from<update.activity_duration_hours){$('#profile-error').textContent='Enter a name and an available range long enough for the whole activity.';return;}
    $('#save-profile').disabled=true;$('#profile-error').textContent='';
    try{await saveProfile(update);$('#profile-dialog').close();const ok=await onSave();toast(ok===false?'Profile saved; weather refresh failed. Retry above.':isMock?'Mock profile saved; weather fixtures stay fixed.':'Profile saved. Outlook and food ideas updated.');}
    catch(error){$('#profile-error').textContent=error.message;}
    finally{$('#save-profile').disabled=false;}
  });
  $('#reset-demo').addEventListener('click',async()=>{
    $('#reset-demo').disabled=true;
    try{await resetSession();resetCallback();clearDismissed();$('#profile-dialog').close();await onSave();toast('Previous profile deleted. A fresh demo is ready.');}
    catch(error){$('#profile-error').textContent=error.message;}
    finally{$('#reset-demo').disabled=false;}
  });
}
