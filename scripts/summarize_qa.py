#!/usr/bin/env python3
import json,hashlib,os
from pathlib import Path
r=Path(__file__).resolve().parents[1]
q=json.loads((r/'output/qa.json').read_text())
result={k:q.get(k) for k in ('url','version','ig-ver','errs','warnings','hints','broken-links')}
result.update(publisher='3.0.1',fhir='5.0.0',ru_core='0.26.0',ru_core_delivery='current',terminology='-tx '+os.environ.get('FHIR_TX_SERVER','https://tx.fhir.org/r5'),bundle_sha256=hashlib.sha256((r/'input/examples/Bundle-semd-amb-consultation-example.json').read_bytes()).hexdigest())
(r/'reports/publisher-summary.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False))
if q.get('errs',1) or q.get('broken-links',1):raise SystemExit('Publisher QA has errors or broken links')
