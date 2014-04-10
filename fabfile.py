from fabric.api import local, run, cd, quiet, abort
from fabric.colors import blue, red, yellow, green
import os
import fabconf
import jinja2


config = dict()
for key in dir(fabconf):
    config[key] = getattr(fabconf, key)


"""
Local Commands
"""


def _setup(f):
    """Global decorator.

    1. Wraps environment variables.
    2. Wraps quiet.
    """
    def decorator(*args, **kwargs):
        # with shell_env(**config):
        #     if 'environ' in inspect.getargspec(f)[0]:
        #         kwargs['environ'] = config
        #     with quiet():
        #         return f(*args, **kwargs)
        with quiet():
            return f(*args, **kwargs)
    return decorator


def _running():
    """Returns whether uwsgi processes are running.
    """
    cmd = "ps aux | grep uwsgi.*%(project_name)s" % config
    r = local(cmd, capture=True).stdout
    return '.ini' in r


def _pid():
    """Returns PID if PID file exists or returns `None`.
    """
    cmd = "cat %(path_run)s/%(uwsgi_pid)s" % config
    pid = local(cmd, capture=True).stdout
    if pid:
        return pid
    return None


def _kill():
    local("ps aux | grep %(uwsgi_config)s | awk '{print $2}' | "
          "xargs kill -9 2>/dev/null" % config)


def _abort(message):
    abort(red(message))


@_setup
def _conf_exists():
    """Returns `False` if there is no file in `CONF` directory.
    """

    conf_gen_path = '%(path_conf_gen)s' % config
    files = [f for f in os.listdir(conf_gen_path) if f[0] != '.']
    return not not files


@_setup
def conf():
    """Compiles configurations
    """

    print blue("* Generating '%(path_conf_gen)s'..." % config),
    local("mkdir %(path_conf_gen)s" % config)
    print blue('Done')

    dir_src = config['path_conf_src']
    dir_gen = config['path_conf_gen']
    for filename in os.listdir(dir_src):
        if filename[0] == '.':
            continue

        print blue("* Configuring '%s'..." % filename),
        input_file = open(os.path.join(dir_src, filename), 'r')
        template = jinja2.Template(input_file.read())
        output_file = open(os.path.join(dir_gen, filename), 'w')
        output_file.write(template.render(**config).encode('utf8'))
        print blue('Done')


@_setup
def nginx():
    """Configure nginx.
    """

    source = '%(path_conf)s/gen/%(nginx_config)s' % config
    target = '/etc/nginx/sites-enabled/%(nginx_config)s' % config

    print blue("* Creating symbolic link..."),
    local('[ -e %s ] && sudo rm %s' % (target, target))
    rv = local('sudo ln -s %s %s' % (source, target))
    if rv.succeeded:
        print blue('Done')
    else:
        print red("Failed")
        _abort(rv.stderr.strip())

    print blue("* Reloading nginx..."),
    rv = local('sudo service nginx reload')
    if rv.succeeded:
        print blue('Done')
    else:
        print red("Failed")
        _abort(rv.stderr.strip())


@_setup
def status():
    running = _running()
    pid = _pid()

    if running and pid:
        print blue("* %(project_name)s is running" % config)

    elif running and not pid:
        print blue("* %(project_name)s is running, "
                   "but has no PID file." % config)

    elif not running and pid:
        print yellow("* %(project_name)s is not running, "
                     "but has PID file." % config)

    elif not running and not pid:
        print yellow("* %(project_name)s is not running" % config)


@_setup
def start():
    if _running():
        _kill()

    if not _conf_exists():
        conf()

    cmd = 'uwsgi %(path_conf_gen)s/%(uwsgi_config)s --enable-threads' % config
    try:
        if config['debug']:
            cmd += ' --catch-exceptions'
            print green("*** DEBUG MODE ENABLED ***")
    except:
        pass

    print blue("* Starting %(project_name)s..." % config),
    rv = local(cmd, capture=True)
    if rv.succeeded:
        print blue("Done")
    else:
        print red("Failed")
        _abort(rv.stderr)


@_setup
def stop():
    running = _running()
    pid = _pid()

    if running and pid:
        print blue("* Stopping..."),
        stop_uwsgi = "uwsgi --stop %(path_run)s/%(project_name)s.pid" % config
        rm_pid = "rm %(path_run)s/%(project_name)s.pid" % config
        if local(stop_uwsgi).succeeded and local(rm_pid).succeeded:
            print blue('Done')
        else:
            print red('Failed')

    elif running and not pid:
        print blue("* %(project_name)s is running, but has no PID file. "
                   "Killing..." % config)
        _kill()
        print blue('Done')

    elif not running and pid:
        print blue("* %(project_name)s is not running, but has PID file. "
                   "Removing..." % config),
        if local('rm %(path_run)s/%(project_name)s.pid' % config).succeeded:
            print blue('Done')
        else:
            print red('Failed')

    elif not running and not pid:
        print yellow("* %(project_name)s is not running" % config)


@_setup
def reload():
    running = _running()
    pid = _pid()

    if running and pid:
        cmd = 'uwsgi --reload %(path_var)s/run/%(project_name)s.pid' % config
        try:
            if config['debug']:
                cmd += ' --catch-exceptions'
                print green("*** DEBUG MODE ENABLED ***")
        except:
            pass
        print blue("* Reloading..."),
        local(cmd)
        print blue('Done')

    elif running and not pid:
        _abort("%(project_name)s running, but has no PID file. "
               "Use 'start' instead." % config)

    elif not running and pid:
        _abort("%(project_name)s is not running, but has PID file. "
               "Use 'start' instead." % config)

    elif not running and not pid:
        _abort("%(project_name)s is not running." % config)


@_setup
def restart():
    stop()
    start()


@_setup
def log(type='uwsgi'):
    """Open a log file.

    :param type: Log type. 'uwsgi'(default), 'nginx.access', 'nginx.error'
    """
    if type == 'uwsgi':
        local('open %(path_log)s/%(uwsgi_log)s' % config)
    elif type == 'nginx.access':
        local('open %(path_log)s/%(nginx_access_log)s' % config)
    elif type == 'nginx.error':
        local('open %(path_log)s/%(nginx_error_log)s' % config)


@_setup
def setup_rmq():
    """Set up rabbitmq server. Add user, add vhost, then set permissions.
    """
    print blue("* Adding user..."),
    if not local("sudo rabbitmqctl add_user '%(rmq_user_name)s' "
                 "'%(rmq_user_password)s'" % config).succeeded:
        print red("Failed"), yellow("(potentially exists already)")
    else:
        print blue("Done")

    print blue("* Adding vhost..."),
    if not local("sudo rabbitmqctl add_vhost '%(rmq_vhost)s'" % config):
        print red("Failed"), yellow("(potentially exists already)")
    else:
        print blue("Done")

    print blue("* Setting permissions..."),
    if not local("sudo rabbitmqctl set_permissions -p '%(rmq_vhost)s' "
                 "'%(rmq_user_name)s' '.*' '.*' '.*'" % config):
        print red("Failed"), yellow("(potentially exists already)")
    else:
        print blue("Done")


@_setup
def celery(cmd=None, worker=None):
    if cmd == 'start':
        r = local("celery multi start %(celery_workers)s"
                  " --hostname=%(celery_hostname)s"
                  " -B -A deuktem.tasks"  # celery beat
                  " --schedule=%(path_celery_schedule)s"
                  " --logfile=%(path_celery_log)s "
                  " --pidfile=%(path_celery_pid)s" % config, capture=True)
        print r.stderr

    elif cmd == 'restart':
        r = local("celery multi restart %(celery_workers)s"
                  " --hostname=%(celery_hostname)s"
                  " -B -A deuktem.tasks"  # celery beat
                  " --schedule=%(path_celery_schedule)s"
                  " --logfile=%(path_celery_log)s "
                  " --pidfile=%(path_celery_pid)s" % config, capture=True)
        print r.stderr

    elif cmd == 'stop':
        print blue("* Killing celery processes..."),
        local("ps aux | grep 'celery worker' | grep '%(project_name)s' | "
              "awk '{print $2}' | xargs kill -9" % config)
        print blue("Done")

        print blue("* Removing pid files..."),
        local("rm %(path_run)s/celery*.pid 2>/dev/null" % config)
        print blue("Done")

    elif cmd == 'status':
        r = local("celery status", capture=True)
        print r.stdout

    else:
        abort(red("Usage: fab celery:[start|restart|stop|log|status]"))


def celery_log(worker=None):
    if worker is None:
        abort(red("Usage: fab celery_log:[worker_number]"))
    conf = config.copy()
    conf.update(worker=worker)
    local("tail -f %(path_log)s/celery%(worker)s.log" % conf)


"""
Deploy Command
"""


"""
Remote Commands
"""


def remote(cmd):
    """Run local commands from remote.

    Usage: %(fab)s remote:start
    """
    with cd('notipy'):
        run('fab ' + cmd)

r = remote
