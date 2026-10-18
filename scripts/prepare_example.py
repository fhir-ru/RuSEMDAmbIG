#!/usr/bin/env python3
"""Add application profiles and readable narratives; retain all clinical facts."""
import json,copy,hashlib,shutil
from pathlib import Path
from narratives import enrich_narratives, human_value, TITLES
ROOT=Path(__file__).resolve().parents[1]
CANONICAL='https://fhir.ru/ig/semd/amb/StructureDefinition/'
PROFILES={'Composition':'semd-amb-composition','MedicationStatement':'semd-amb-medication-statement','MedicationAdministration':'semd-amb-medication-administration'}
def prepare(bundle):
    out=copy.deepcopy(bundle)
    out['id']='semd-amb-consultation-example'
    out['meta']['profile']=[CANONICAL+'semd-amb-bundle']
    for e in out['entry']:
        r=e['resource']
        if r['resourceType'] in PROFILES:
            r.setdefault('meta',{})['profile']=[CANONICAL+PROFILES[r['resourceType']]]
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
