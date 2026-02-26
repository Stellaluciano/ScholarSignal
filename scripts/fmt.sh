#!/usr/bin/env bash
set -euo pipefail
cd backend && python -m ruff format .
