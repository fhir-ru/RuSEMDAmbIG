#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
PYTHON_BIN="${PYTHON_BIN:-python3}"
"$PYTHON_BIN" scripts/clean_generated.py
"$PYTHON_BIN" scripts/fetch_dependency.py
"$PYTHON_BIN" scripts/convert.py
"$PYTHON_BIN" scripts/verify_mapping.py
"$PYTHON_BIN" scripts/generate_content_profiles.py
"$PYTHON_BIN" scripts/prepare_example.py
bash run_sushi.sh
if [[ ! -s input-cache/publisher.jar ]]; then
  mkdir -p input-cache
  curl -fL https://github.com/HL7/fhir-ig-publisher/releases/download/3.0.1/publisher.jar -o input-cache/publisher.jar
fi
mkdir -p reports input-cache/profile-rule-classes
javac -proc:none -cp input-cache/publisher.jar -d input-cache/profile-rule-classes scripts/CheckProfileRules.java
java -cp input-cache/publisher.jar:input-cache/profile-rule-classes CheckProfileRules "${FHIR_PACKAGE_CACHE:-$HOME/.fhir/packages}/hl7.fhir.r5.core#5.0.0"
java -Xmx4g -Dfile.encoding=UTF-8 -jar input-cache/publisher.jar -ig ig.ini -tx "${FHIR_TX_SERVER:-https://tx.fhir.org/r5}" "$@" 2>&1 | tee reports/publisher.log
"$PYTHON_BIN" scripts/summarize_qa.py
"$PYTHON_BIN" scripts/audit_qa.py
