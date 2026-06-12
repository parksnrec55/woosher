#!/bin/bash
set -e

HOST=${HOST:-0.0.0.0}
PORT=${PORT:-8000}
WORKERS=${WORKERS:-4}

exec uvicorn main:app --host "$HOST" --port "$PORT" --workers "$WORKERS"
