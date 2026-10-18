#!/usr/bin/env python3
"""Classify Publisher QA without suppressing messages or changing severities."""
import collections
import hashlib
import json
import pathlib
import re
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parents[1]
NS = {'f': 'http://hl7.org/fhir'}

def val(node, path, default=''):
    element = node.find(path, NS)
    return element.get('value', default) if element is not None else default


def category(message):
    if any(token in message for token in ('CodeSystem', 'code system', 'No definition could be found for URL', 'versionless include', 'Не удалось найти определение для значения URL')):
        return 'external_codes_and_versions'
    if any(token in message for token in ('HTML', 'XHTML', 'lang tag', 'description for the resource', 'history.html', 'fragment', 'page named')):
        return 'html_and_publication'
    return 'profiles_and_examples'


def main():
    summary = json.loads((ROOT/'output/qa.json').read_text())
    tree = ET.parse(ROOT/'output/qa.xml')
    issues = []
    for outcome in tree.findall('.//f:OperationOutcome', NS):
        filename = ''
        for extension in outcome.findall('f:extension', NS):
            if extension.get('url', '').endswith('operationoutcome-file'):
                filename = val(extension, 'f:valueString')
        for issue in outcome.findall('f:issue', NS):
            message = val(issue, 'f:details/f:text')
            extensions = {}
            for extension in issue.findall('f:extension', NS):
                key = extension.get('url', '').rsplit('/', 1)[-1]
                child = list(extension)
                extensions[key] = child[0].get('value', '') if child else ''
            issues.append({'severity': val(issue,'f:severity'), 'message': message,
                           'category': category(message), 'file': filename,
                           'expressions': [e.get('value') for e in issue.findall('f:expression',NS)],
                           'extensions': extensions, 'source': 'output/qa.xml'})
    # Publisher's XML omits build-level issues. Read ONLY the n/a build block
    # from the companion qa.txt to reconcile all unsuppressed warning counts.
    text = (ROOT/'output/qa.txt').read_text()
    build = re.search(r'== n/a ==\s*(.*?)(?=\n== |\Z)', text, flags=re.S)
    if build:
        for severity, message in re.findall(r'^(ERROR|WARNING|INFORMATION): (.*)$',build.group(1),flags=re.M):
            issues.append({'severity': {'ERROR':'error','WARNING':'warning','INFORMATION':'information'}[severity],
                           'message': message.rstrip(), 'category': category(message),
                           'source': 'output/qa.txt build section'})
    counts = collections.Counter(item['severity'] for item in issues)
    expected = {'error': summary['errs'], 'warning': summary['warnings'], 'information': summary['hints']}
    if dict(counts) != {key:value for key,value in expected.items() if value}:
        raise SystemExit('QA reconciliation mismatch: '+repr(dict(counts))+' vs '+repr(expected))
    if summary.get('suppressed-warnings',0) or summary.get('suppressed-hints',0):
        raise SystemExit('Suppressed messages exist: this report assumes unsuppressed QA')
    groups = {}
    for item in issues:
        key = (item['severity'],item['category'],item['message'])
        groups.setdefault(key,[]).append({key:value for key,value in item.items() if key not in ('severity','category','message')})
    grouped = [{'severity':severity,'category':cat,'message':message,'count':len(instances),'instances':instances}
               for (severity,cat,message),instances in groups.items()]
    warnings = [item for item in issues if item['severity']=='warning']
    report = {'scope':'Independent classification of exact, unsuppressed Publisher QA messages; no severity changed and no warning suppressed.',
              'qa': summary, 'counts_reconciled': dict(counts),
              'warning_categories': dict(collections.Counter(item['category'] for item in warnings)),
              'source_sha256': {name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
                                for name in ('output/qa.xml','output/qa.json','output/qa.txt')},
              'notes': ['qa.xml omits build issues; qa.txt n/a block supplies those without duplicating resource issues.',
                        'Bundle and individual resource examples cause repeated resource warnings.',
                        'Unknown code systems/versions are unverified, not proven invalid.',
                        'Source NSI versions on RuCore canonical Coding are a known version-model mismatch, distinct from unknown external OID systems.',
                        'Missing Observation performers/effective times and attachment content metadata must not be invented from absent source facts.'],
              'groups': grouped}
    (ROOT/'reports/qa-review.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'counts':dict(counts),'warning_categories':report['warning_categories'],'groups':len(grouped)},ensure_ascii=False))

if __name__=='__main__':
    main()
