#!/usr/bin/env python3
"""Add application profiles and readable narratives; retain all clinical facts."""
import json,copy,hashlib,shutil
from pathlib import Path
from narratives import enrich_narratives, human_value, TITLES
ROOT=Path(__file__).resolve().parents[1]
CANONICAL='https://fhir.ru/ig/semd/amb/StructureDefinition/'
PROFILES={'Composition':'semd-amb-composition','MedicationStatement':'semd-amb-medication-statement','MedicationAdministration':'semd-amb-medication-administration'}
CATALOG=json.loads((ROOT/'spec/edition7-content.json').read_text())
for resource in ('Patient','Organization','Practitioner','PractitionerRole','Encounter','Coverage','Condition','AllergyIntolerance','Procedure','CarePlan','DocumentReference','Medication'):
    import re
    slug=re.sub(r'(?<!^)(?=[A-Z])','-',resource).lower()
    PROFILES[resource]='semd-amb-'+slug
PROFILES['PractitionerRole']='semd-amb-practitioner-role'

def code(resource):
    return next((c.get('code') for c in resource.get('code',{}).get('coding',[])),None)

def prepare(bundle):
    out=copy.deepcopy(bundle)
    out['id']='semd-amb-consultation-example'
    out['meta']['profile']=[CANONICAL+'semd-amb-bundle']
    for e in out['entry']:
        r=e['resource']
        if r['resourceType'] in PROFILES:
            r.setdefault('meta',{})['profile']=[CANONICAL+PROFILES[r['resourceType']]]
    resources={e['fullUrl']:e['resource'] for e in out['entry']}
    for resource in resources.values():
        if resource['resourceType']=='Observation':
            c=code(resource)
            qualifier=next((q for q in CATALOG['qualifiers'] if q['code']==c),None)
            resource.setdefault('meta',{})['profile']=[CANONICAL+('semd-amb-qualifier-'+c if qualifier else 'semd-amb-observation')]
    composition=next(r for r in resources.values() if r['resourceType']=='Composition')
    context=composition['section'][-1]
    roles={'Получатель документа':'recipient','Источник оплаты консультации':'payment','Направившее лицо':'referrer','Документ направления':'referral'}
    for subsection in context.get('section',[]):
        role=roles.get(subsection.get('title'))
        if role:subsection.setdefault('extension',[]).append({'url':CANONICAL+'semd-amb-context-role','valueCode':role})
    event=next(reference for reference in context.get('entry',[]) if resources[reference['reference']]['resourceType']=='Procedure')
    context.setdefault('section',[]).insert(0,{'title':'Документируемое событие','extension':[{'url':CANONICAL+'semd-amb-context-role','valueCode':'document-event'}], 'text':{'status':'generated','div':'<div xmlns="http://www.w3.org/1999/xhtml"><p>Документируемое событие консультации</p></div>'},'entry':[copy.deepcopy(event)]})
    for reference in composition['author']:
        role=resources[reference['reference']]
        role['meta']['profile']=[CANONICAL+'semd-amb-author-role']
        person=resources[role['practitioner']['reference']]
        person['meta']['profile']=[CANONICAL+'semd-amb-author-practitioner']
    for section in composition['section']:
        section_code=code(section)
        candidates=[e for e in CATALOG['entries'] if e['section']==section_code and e['resource']=='Observation']
        for reference in section.get('entry',[]):
            resource=resources[reference['reference']]
            if section_code=='LINKDOCS' and resource['resourceType']=='DocumentReference':
                resource['meta']['profile']=[CANONICAL+'semd-amb-linked-document']
            if resource['resourceType']!='Observation':continue
            entry=next((e for e in candidates if e['code']==code(resource)),None)
            if entry is None and len(candidates)==1 and candidates[0]['code'] is None:entry=candidates[0]
            if entry:resource['meta']['profile']=[CANONICAL+'semd-amb-entry-'+str(entry['number'])]
    return enrich_narratives(out)
def main():
    original=json.loads((ROOT/'examples/consultation-bundle.json').read_text())
    out=prepare(original)
    (ROOT/'input/examples/Bundle-semd-amb-consultation-example.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    # Standalone nested resources help readers navigate and Publisher resolve references.
    for e in out['entry']:
        r=e['resource']
        (ROOT/'input/examples'/f"{r['resourceType']}-{r['id']}.json").write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
    for name in ('mapping.tsv','trace.json','summary.json'):
        shutil.copyfile(ROOT/'examples'/name,ROOT/'input/assets'/name)
    shutil.copyfile(ROOT/'source/consultation.xml',ROOT/'input/assets/consultation-source.xml')
    config=ROOT/'sushi-config.yaml'
    config_text=config.read_text().split('\nresources:\n')[0].rstrip()+'\nresources:\n'
    for e in out['entry']:
        resource=e['resource']
        key=resource['resourceType']+'/'+resource['id']
        name=resource['resourceType']+' '+resource['id'][:8]
        description=TITLES.get(resource['resourceType'],resource['resourceType'])
        for field in ('code','title','description','name'):
            if resource.get(field):
                description+=': '+human_value(resource[field]);break
        config_text+='  '+json.dumps(key)+':\n    name: '+json.dumps(name,ensure_ascii=False)+'\n    description: '+json.dumps(description,ensure_ascii=False)+'\n'
    config_text+='  Bundle/semd-amb-consultation-example:\n    name: Протокол консультации редакции 7 — учебный пример\n'
    config.write_text(config_text)
    print(json.dumps({'prepared_resources':len(out['entry']),'application_profiles':PROFILES},ensure_ascii=False))
if __name__=='__main__':main()
