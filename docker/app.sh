#!/bin/bash

alembic upgrade head

if [ "$ENV" = "TEST" ]; then
  pytest
else
  gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
fi