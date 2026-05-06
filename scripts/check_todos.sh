#!/usr/bin/env bash
set -euo pipefail
grep -R "TODO(student)" -n src tests docs \
  --exclude-dir='__pycache__' \
  --exclude-dir='*.egg-info' \
  --exclude='*.pyc' || true
