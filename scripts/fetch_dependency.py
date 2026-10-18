#!/usr/bin/env python3
"""Install the frozen official RuCore package without mutable CI dependencies."""
from pathlib import Path
import hashlib,json,tarfile
r=Path(__file__).resolve().parents[1]
lock=json.loads((r/'dependencies/lock.json').read_text())['ru.core']
archive=r/'dependencies'/lock['file']
assert hashlib.sha256(archive.read_bytes()).hexdigest()==lock['sha256'],'Dependency checksum mismatch'
with tarfile.open(archive) as t:
    package=json.load(t.extractfile('package/package.json'))
    assert package['name']=='ru.core' and package['version']==lock['version']
    base=Path.home()/('.fhir/packages/ru.core#'+lock['version'])
    present=base/'package/package.json'
    if present.exists() and json.loads(present.read_text())==package:
        print('Using cached official ru.core'+lock['version']);raise SystemExit(0)
    base.mkdir(parents=True,exist_ok=True)
    for m in t.getmembers():
        assert (base/m.name).resolve().is_relative_to(base.resolve()) and not m.issym() and not m.islnk()
    t.extractall(base,filter='data')
print('Installed frozen official ru.core'+lock['version'])
