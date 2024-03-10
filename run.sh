#!/usr/bin/env bash

python -m gunicorn backend.app:app run -b 0.0.0.0:8080