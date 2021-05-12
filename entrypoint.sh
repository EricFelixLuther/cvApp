#!/bin/bash

python /code/cv_App/manage.py collectstatic -c --noinput
python /code/cv_App/manage.py migrate

exec "$@"
