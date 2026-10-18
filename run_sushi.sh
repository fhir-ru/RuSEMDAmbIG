#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
sushi . 2>&1 | tee sushi_output.txt
