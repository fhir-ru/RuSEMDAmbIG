#!/usr/bin/env python3
"""Independent checks of the single frozen edition-7 example, not all guide variants."""
import base64, hashlib, importlib.util, json, re, zipfile
from pathlib import Path
from lxml import etree as E

ROOT = Path(__file__).resolve().parents[1]
NS = {'cda':'urn:hl7-org:v3', 'xsi':'http://www.w3.org/2001/XMLSchema-instance',
      'identity':'urn:hl7-ru:identity','address':'urn:hl7-ru:address',
      'fias':'urn:hl7-ru:fias','medService':'urn:hl7-ru:medService'}
C = '{urn:hl7-org:v3}'; X = '{http://www.w3.org/2001/XMLSchema-instance}'

def date(value):
    m=re.fullmatch(r'(\d{4})(\d{2})(\d{2})(?:(\d{2})(\d{2})(\d{2})?([+-]\d{4}|Z))?', value)
    assert m, value
    y,mo,d,h,mi,s,z=m.groups(); result=f'{y}-{mo}-{d}'
    if h:
        result+=f'T{h}:{mi}:{s or "00"}' + (z if z=='Z' else z[:3]+':'+z[3:])
    return result

def coding(cc, code, system_suffix=None):
    return any(c.get('code')==code and (system_suffix is None or c.get('system','').endswith(system_suffix)) for c in cc.get('coding',[]))

def main():
    checks=[]
    def check(name, action):
        try:
            detail=action()
            checks.append({'name':name,'passed':True,'detail':detail})
        except Exception as exc:
            checks.append({'name':name,'passed':False,'error':type(exc).__name__+': '+str(exc)})
    def require(condition, message):
        assert condition, message
    source=ROOT/'source/consultation.xml'; raw=source.read_bytes()
    manifest=json.loads((ROOT/'source/manifest.json').read_text())
    doc=E.fromstring(raw,E.XMLParser(remove_comments=True,resolve_entities=False,no_network=True))
    bundle=json.loads((ROOT/'examples/consultation-bundle.json').read_text())
    trace=json.loads((ROOT/'examples/trace.json').read_text())
    resources=[entry['resource'] for entry in bundle['entry']]
    by_url={entry['fullUrl']:entry['resource'] for entry in bundle['entry']}
    by_key={r['resourceType']+'/'+r['id']:r for r in resources}
    def target(pointer):
        key,ptr=pointer.split('#',1); value=bundle if key=='Bundle' else by_key[key]
        for token in ptr.strip('/').split('/') if ptr.strip('/') else []:
            token=token.replace('~1','/').replace('~0','~')
            value=value[int(token)] if isinstance(value,list) else value[token]
        return value
    def section(code):
        rows=doc.xpath('.//cda:section[cda:code/@code="'+code+'"]',namespaces=NS)
        assert len(rows)==1, (code,len(rows));return rows[0]
    def source_target(node, attr):
        values=[row for row in trace if row['value']==node.get(attr) and len(doc.xpath(row['xpath'],namespaces=NS))==1 and getattr(doc.xpath(row['xpath'],namespaces=NS)[0],'getparent',lambda:None)()==node]
        assert len(values)==1,(attr,node.attrib,values)
        assert values[0]['targets'],values[0]
        return [target(t) for t in values[0]['targets']]
    def hashes():
        require(hashlib.sha256(raw).hexdigest()==manifest['source_xml_sha256'],'XML hash mismatch')
        return {'xml_sha256':manifest['source_xml_sha256'],'original_archive_sha256':manifest['archive_sha256'],'scope':'XML only; archive provenance verified before extraction in RuCore experiment'}
    check('frozen_source_and_manifest_integrity',hashes)
    def determinism():
        spec=importlib.util.spec_from_file_location('edition7_converter',ROOT/'scripts/convert.py')
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        first=module.Conversion(source,manifest['assembled_at']).build()
        second=module.Conversion(source,manifest['assembled_at']).build()
        require(first==second==bundle,'Repeated/imported conversion differs from frozen output')
        return 'Two fresh imported conversions equal saved Bundle'
    check('deterministic_conversion',determinism)
    def scalars():
        source_count=sum(len(n.attrib)+bool(n.text and n.text.strip())+bool(n.tail and n.tail.strip()) for n in doc.iter())
        require(len(trace)==len({r['xpath'] for r in trace})==source_count,'Trace is not exhaustive/unique')
        count=0
        for row in trace:
            values=doc.xpath(row['xpath'],namespaces=NS)
            require(len(values)==1 and str(values[0]).strip()==row['value'],row['xpath'])
            for pointer in row['targets']:target(pointer);count+=1
        return {'source_scalars':source_count,'resolved_targets':count}
    check('all_source_scalars_and_trace_targets_resolve',scalars)
    def observation_roles():
        source_roles=doc.xpath('.//cda:observation/cda:performer/cda:modeCode',namespaces=NS)
        destination_roles=[]
        for resource in resources:
            if resource['resourceType']!='Observation':continue
            for performer in resource.get('performer',[]):
                for extension in performer.get('extension',[]):
                    if extension['url'].endswith('semd-amb-participant-role'):
                        destination_roles.extend(extension['valueCodeableConcept'].get('coding',[]))
        expected=[{'system':'urn:oid:'+node.get('codeSystem'),'code':node.get('code'),
                   'version':node.get('codeSystemVersion'),'display':node.get('displayName')} for node in source_roles]
        require(destination_roles==expected,'Observation participant roles lost or changed')
        return {'roles_preserved':len(expected),'position_is_separate':True}
    check('observation_participant_roles_preserve_coding',observation_roles)

    references=[]
    def walk(v):
        if isinstance(v,dict):
            if isinstance(v.get('reference'),str):references.append(v['reference'])
            for x in v.values():walk(x)
        elif isinstance(v,list):
            for x in v:walk(x)
    walk(bundle)
    def closure():
        require(len(by_url)==len(by_key)==len(resources),'Duplicate URL/resource identity')
        require(all(r in by_url for r in references),'Dangling reference')
        return {'resources':len(resources),'references':len(references)}
    check('resource_identity_unique_and_references_closed',closure)
    def sections_and_text():
        source_sections=doc.xpath('.//cda:section',namespaces=NS)
        require(len(source_sections)==20,'Not the frozen 20-section example')
        comp=resources[0];require(comp['resourceType']=='Composition','Composition not first')
        found=[]
        def descend(items):
            for s in items:
                if s.get('code'):found.extend(c['code'] for c in s['code'].get('coding',[]))
                descend(s.get('section',[]))
        descend(comp['section'])
        expected=[s.find(C+'code').get('code') for s in source_sections]
        require(all(found.count(code)==1 for code in expected),'Source section lost/duplicated')
        st=doc.xpath('.//cda:value[@xsi:type="ST"]',namespaces=NS)
        for n in st:
            rows=[r for r in trace if '/text()' in r['xpath'] and len(doc.xpath(r['xpath'],namespaces=NS))==1 and getattr(doc.xpath(r['xpath'],namespaces=NS)[0],'getparent',lambda:None)()==n]
            require(len(rows)==1 and rows[0]['targets'],'ST missing structured destination')
            require(any(target(t)==(n.text or '').strip() for t in rows[0]['targets']),'ST content changed')
        return {'sections':len(source_sections),'ST_values':len(st)}
    check('all_sections_and_ST_content_preserved',sections_and_text)
    encounter=next(r for r in resources if r['resourceType']=='Encounter')
    def diagnoses():
        conditions=[r for r in resources if r['resourceType']=='Condition']
        require(len(conditions)==2,'Expected two Conditions')
        expected={'I11.9':'1','H35.0':'2'}
        for condition in conditions:
            code=next(c['code'] for c in condition['code']['coding'] if c['code'] in expected)
            require(condition.get('recordedDate')=='2025-05-02','Diagnosis date lost')
            require(by_url[condition['encounter']['reference']] is encounter,'Condition Encounter lost')
            links=[d for d in encounter['diagnosis'] if any(x.get('reference',{}).get('reference')=='urn:uuid:'+condition['id'] for x in d['condition'])]
            require(len(links)==1,'Diagnosis Encounter association missing')
            axes=links[0]['use'];require(len(axes)==2,'Independent diagnosis axes collapsed')
            require(any(coding(a,expected[code],'core-cs-nsi-diagnosis-nosology-kind') for a in axes),'Nosology axis lost')
            require(any(coding(a,'3','core-cs-nsi-diagnosis-justification-degree') for a in axes),'Justification axis lost')
        return sorted(expected)
    check('two_conditions_encounter_axes_and_date',diagnoses)
    def service():
        node=section('SERVICES').find(C+'entry/'+C+'observation')
        value=node.find(C+'value'); event=next(r for r in resources if r['resourceType']=='Procedure' and coding(r.get('code',{}),value.get('code')))
        require(event['occurrenceDateTime']==date(node.find(C+'effectiveTime').get('value')),'Service time changed')
        require(by_url[event['encounter']['reference']] is encounter,'Service encounter lost')
        require('recorder' not in event,'Recorder inferred without source AUTHOR')
        return {'code':value.get('code'),'time':event['occurrenceDateTime']}
    check('direct_service_code_time_no_invented_recorder',service)
    def local_links():
        source_docs={}
        for act in section('LINKDOCS').xpath('cda:entry/cda:act',namespaces=NS):
            ident=act.find(C+'id'); key=(ident.get('root'),ident.get('extension'));require(key not in source_docs,'Duplicate source local II');source_docs[key]=act
        links=doc.xpath('.//cda:entryRelationship[@typeCode="REFR"]/cda:act/cda:id',namespaces=NS)
        require(len(links)==3,'Expected three REFRs')
        for ident in links:
            key=(ident.get('root'),ident.get('extension'));require(key in source_docs,'Unresolved full local II')
            # Trace resolves the original root+extension together to the actual resource.
            destinations=source_target(ident,'extension')
            require(len(destinations)==1,'Ambiguous REFR mapping')
            ref=destinations[0];require(isinstance(ref,dict) and ref.get('reference') in by_url,'REFR target not a resource reference')
            resource=by_url[ref['reference']];require(resource['resourceType']=='DocumentReference','REFR not DocumentReference')
            source_act=source_docs[key];expected_type=source_act.find(C+'code').get('code')
            require(coding(resource['type'],expected_type),'REFR resolved to wrong document type')
            require(resource['content'][0]['attachment']['creation']==date(source_act.find(C+'effectiveTime').get('value')),'Linked document date lost')
            source_number=source_act.xpath('cda:entryRelationship/cda:observation[cda:code/@code="11003"]/cda:value/text()',namespaces=NS)[0]
            require(resource.get('description')==source_number or any(i.get('value')==source_number for i in resource.get('identifier',[])),'Linked document number mismatch')
        return {'resolved_full_II_links':len(links),'LINKDOCS_records':len(source_docs)}
    check('three_REFR_links_resolve_full_local_II',local_links)
    def disability():
        obs=next(r for r in resources if r['resourceType']=='Observation' and coding(r.get('code',{}),'814'))
        require(obs['effectivePeriod']['start']=='2014-10-22','Disability start lost')
        end=obs['effectivePeriod'].get('_end',{})
        require(any(e.get('valueCode')=='PINF' and e.get('url','').endswith('iso21090-nullFlavor') for e in end.get('extension',[])),'PINF not preserved')
        require('end' not in obs['effectivePeriod'] and not any(e.get('valueCode')=='unknown' for e in end.get('extension',[])),'PINF changed to unknown/concrete end')
        return 'Known start and explicitly unbounded end retained'
    check('disability_PINF_not_unknown',disability)
    def imm():
        node=section('IMM').find(C+'entry/'+C+'observation');code=node.find(C+'code')
        candidates=[r for r in resources if r['resourceType']=='MedicationAdministration' and coding(r.get('medication',{}).get('concept',{}),code.get('code'),code.get('codeSystem'))]
        require(len(candidates)==1,'IMM administration lost')
        item=candidates[0]
        require(item['status']=='completed' and item['subject']==encounter['subject'],'Application fact or patient lost')
        require(item['medication']['concept']['coding']==[{'system':'urn:oid:'+code.get('codeSystem'), 'code':code.get('code'), 'version':code.get('codeSystemVersion'), 'display':code.get('displayName')}], 'Product metadata changed')
        require(item['occurenceDateTime']==date(node.find(C+'effectiveTime').get('value'))=='2025-05-01','Application date lost')
        require(not any(k in item for k in ['encounter','dosage','performer','reason','partOf','occurrenceDateTime']), 'Invented context/dose/performer or wrong R5 field')
        require(not any(r['resourceType']=='Immunization' for r in resources),'Diagnostic allergen turned into vaccination')
        require(not any(r['resourceType']=='Observation' and coding(r.get('code',{}),code.get('code'),code.get('codeSystem')) for r in resources),'Duplicate generic drug Observation retained')
        for key in ['code','codeSystem','displayName','codeSystemVersion']:
            source_target(code,key)
        section_entry=next(s for s in resources[0]['section'] if coding(s['code'],'IMM'))
        require(any(by_url[e['reference']]['id']==item['id'] for e in section_entry['entry']),'IMM document entry not linked to administration')
        spec=importlib.util.spec_from_file_location('imm_guard_conversion', ROOT/'scripts/convert.py')
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        unknown=module.Conversion(source,manifest['assembled_at'])
        drug=unknown.doc.xpath('.//cda:section[cda:code/@code="IMM"]/cda:entry/cda:observation/cda:code',namespaces=NS)[0]
        drug.set('code','UNVERIFIED')
        try:unknown.build()
        except ValueError as exc:require('classification is unverified' in str(exc),'Unrelated negative-control failure')
        else:raise AssertionError('Unverified IMM product was classified automatically')
        return {'resource':'MedicationAdministration','code_retained':code.get('code'),'date_retained':item['occurenceDateTime'],'encounter':None,'unknown_product_control':'explicit rejection'}
    check('diagnostic_allergen_administration_without_consultation_encounter',imm)
    def medication():
        item=next(r for r in resources if r['resourceType']=='MedicationStatement');dose=item['dosage'][0]['doseAndRate'][0]['doseQuantity']
        require(dose.get('value')==1 and not any(k in dose for k in ['unit','system','code']),'Dose unit invented')
        repeat=item['dosage'][0]['timing']['repeat'];require(repeat['period']==12 and repeat['periodUnit']=='h','12 h interval not retained')
        require(item['dosage'][0].get('text')=='Разовая доза — 1 потребительская единица указанного препарата (количество в единицах выбранного узла СМНН).','Consumer-unit dose explanation missing')
        require(item['medication']['concept']['coding'][0]['system']=='urn:oid:1.2.643.5.1.13.13.99.2.611','Dose context is not SMNN')
        return {'dose':dose,'text':item['dosage'][0]['text'],'period':repeat['period'],'periodUnit':repeat['periodUnit']}
    check('dose_has_no_invented_unit_and_period_is_hours',medication)
    def card_reference():
        numbers=doc.xpath('cda:componentOf/cda:encompassingEncounter/medService:DocNumber/text()',namespaces=NS)
        require(numbers==['5499-16'],'Source card number changed')
        require(not doc.xpath('cda:componentOf/cda:encompassingEncounter/cda:id[substring(@root,string-length(@root)-2)=".17"]',namespaces=NS),'Unexpected source card II')
        parent=encounter['partOf']; ident=parent['identifier']
        require(parent['type']=='Encounter' and ident['value']==numbers[0], 'Card logical reference missing')
        require(parent['display']=='Амбулаторная медицинская карта № 5499-16','Card display lost')
        require(ident['type']['coding']==[{'system':'urn:oid:1.2.643.5.1.13.13.99.2.723',
                 'code':'1','display':'Амбулаторная медицинская карта','version':'1.1'}], 'Source card type not retained exactly')
        require('system' not in ident and 'assigner' not in ident and 'reference' not in parent, 'Card namespace, issuer or literal reference invented')
        require(len([r for r in resources if r['resourceType']=='Encounter'])==1, 'Parent Encounter invented')
        rows=[r for r in trace if 'medService:DocNumber' in r['xpath']]
        require(len(rows)==1 and rows[0]['status']!='report-only' and any(t.endswith('/partOf/identifier/value') for t in rows[0]['targets']), 'Card number trace not resolved')
        spec=importlib.util.spec_from_file_location('card_negative_conversion', ROOT/'scripts/convert.py')
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        missing=module.Conversion(source,manifest['assembled_at'])
        enc=missing.doc.find('cda:componentOf/cda:encompassingEncounter',NS)
        enc.remove(enc.find('medService:DocNumber',NS))
        result=missing.build()
        require('partOf' not in next(e['resource'] for e in result['entry'] if e['resource']['resourceType']=='Encounter'), 'Card number inferred when absent')
        return {'number':'5499-16','source_type':ident['type'],'system_supplied':False,'missing_number_control':'no partOf inferred'}
    check('card_logical_reference_without_invented_namespace',card_reference)
    def dose_rule_controls():
        spec=importlib.util.spec_from_file_location('dose_rule_conversion', ROOT/'scripts/convert.py')
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        for supplied_unit, system in [('mg','1.2.643.5.1.13.13.99.2.611'),(None,'1.2.3.4')]:
            conversion=module.Conversion(source,manifest['assembled_at'])
            drug=conversion.doc.xpath('.//cda:section[cda:code/@code="DRUG"]/cda:entry/cda:substanceAdministration',namespaces=NS)[0]
            if supplied_unit:drug.find(C+'doseQuantity').set('unit',supplied_unit)
            drug.find(C+'consumable/'+C+'manufacturedProduct/'+C+'manufacturedMaterial/'+C+'code').set('codeSystem',system)
            output=conversion.build()
            dosage=next(e['resource'] for e in output['entry'] if e['resource']['resourceType']=='MedicationStatement')['dosage'][0]
            require('text' not in dosage,'Consumer-unit rule applied outside SMNN dose without unit')
        return {'controls':'explicit unit and other code system do not receive consumer-unit explanation'}
    check('consumer_unit_rule_has_explicit_scope',dose_rule_controls)
    def exact_source():
        refs=[r for r in resources if r['resourceType']=='DocumentReference' and r.get('description','').startswith('Исходный учебный XML')]
        require(len(refs)==1 and base64.b64decode(refs[0]['content'][0]['attachment']['data'])==raw,'Embedded source differs')
    check('original_XML_embedded_byte_exact',exact_source)
    result={'scope':'Single frozen official edition-7 XML example; this is not a FHIR Validator result and does not demonstrate coverage of all guide variants.',
            'passed':all(c['passed'] for c in checks),'checks':checks,
            'unresolved_semantic_gaps':[]}
    (ROOT/'reports/verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'passed':result['passed'],'checks':len(checks),'failures':[c for c in checks if not c['passed']]},ensure_ascii=False))
    return 0 if result['passed'] else 1

if __name__=='__main__':
    raise SystemExit(main())
