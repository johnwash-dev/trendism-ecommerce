#!/usr/bin/env bash
# Error vandha udane stop panna
set -o errexit

# Requirements install panna
pip install -r requirements.txt

# Static files gather panna (CSS/JS load aaga)
python manage.py collectstatic --no-input

# Database migrations run panna
python manage.py migrate