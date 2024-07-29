#!/bin/bash

alembic upgrade head

if [ "$MODE" = "TEST" ]; then
  pytest
else
  gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
fi