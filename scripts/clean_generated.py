#!/usr/bin/env python3
"""Remove only task-generated Publisher directories before a reproducible build."""
from pathlib import Path
import shutil
r=Path(__file__).resolve().parents[1]
for name in ('output','temp'):
    p=r/name
    if p.is_symlink():raise SystemExit('Refusing to clean symlink: '+name)
    if p.is_dir():shutil.rmtree(p)
