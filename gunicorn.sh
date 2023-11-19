#!/bin/bash
source /var/www/DjangoBlog/env/bin/activate
exec gunicorn -c "/var/www/DjangoBlog/mysite/gunicorn_config.py" mysite.wsgi