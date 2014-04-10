from os.path import abspath, join

debug = True

project_name = 'deuktem'

"""
Path
"""
path_root = abspath(join(__file__, '..', '..'))
path_var = join(path_root, 'var')
path_log = join(path_var, 'log')
path_run = join(path_var, 'run')
path_upload = join(path_var, 'upload')
path_conf = join(path_root, project_name, 'conf')
path_conf_src = join(path_conf, 'src')
path_conf_gen = join(path_conf, 'gen')
path_static = join(path_root, project_name, 'static')
path_venv = join(path_root, 'venv')
path_celery_log = join(path_log, 'celery%n.log')
path_celery_pid = join(path_run, 'celery%n.pid')


"""
uWSGI
"""
uwsgi_config = '%s.uwsgi.ini' % project_name
uwsgi_socket = '%s.uwsgi.sock' % project_name
uwsgi_pid = '%s.pid' % project_name
uwsgi_log = '%s.uwsgi.log' % project_name

"""
Nginx
"""
nginx_config = '%s.nginx.conf' % project_name
nginx_listen = 80
nginx_server_name = 'deuktem.joyfl.net *.deuktem.joyfl.net'
nginx_access_log = '%s.nginx.access.log' % project_name
nginx_error_log = '%s.nginx.error.log' % project_name


"""
RabbitMQ
"""
rmq_user_name = 'deuktem'
rmq_user_password = ''
rmq_vhost = 'deuktem'


"""
Celery
"""
celery_workers = 4
celery_name_prefix = 'deuktem'
celery_hostname = 'deuktem.joyfl.net'
