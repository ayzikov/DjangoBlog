command = '/var/www/DjangoBlog/env/bin/gunicorn'
python_path = '/var/www/DjangoBlog/mysite'
bind = '0.0.0.0:8001'
workers = 5
user = 'www'
raw_env = 'DJANGO_SETTINGS_MODULE=mysite.settings'
