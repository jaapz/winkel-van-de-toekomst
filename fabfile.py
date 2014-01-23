import os
from fabric.api import sudo, env, run, cd, settings, hide, shell_env
from fabvenv import virtualenv

env.directory = '/var/www/winkel-van-de-toekomst'
env.venv = '/var/www/winkel-van-de-toekomst/.env'
env.version = 'master'


def prod():
    """ Deploy to servers in production.

    Sets the deploy version to master.
    """
    env.hosts = ['www.dibsop.nl']
    env.version = 'master'


def local():
    """ Deploys to the localhost.

    Sets the deploy version to develop by default.
    """
    env.hosts = ['localhost']
    env.version = 'develop'
    env.directory = os.environ['WINKEL_DIR']
    env.venv = os.environ['WINKEL_VENV']


def restart_webserver():
    """ Restart nginx. """
    sudo('service nginx restart')


def stop_webserver():
    """ Stop nginx. """
    sudo('service nginx stop')


def kill_uwsgi(warn_only=True):
    """ Kill the uwsgi app. """
    with settings(
        hide('warnings', 'running', 'stdout', 'stderr'),
        warn_only=True
    ):
        run('pkill uwsgi')


def remove_tmp_files():
    """ Remove all temporary files, like sockets. """
    sudo('rm -rfv /tmp/winkel.*')


def checkout_version(version=None):
    """ Switch to the given version.

    The version can be anything that `git checkout` accepts as a parameter.
    """
    if version is None:
        version = env.version

    with cd('/var/www/winkel-van-de-toekomst'):
        # Switch to master so we can fetch and pull.
        run('git checkout master')
        run('git fetch')
        run('git pull')
        run('git checkout %s' % version)


def restart_uwsgi():
    """ Restart the uwsgi app as a background task. """
    with virtualenv(env.venv):
        run('uwsgi --emperor /etc/uwsgi/apps-enabled '
            '--daemonize /var/log/winkel.log')


def deploy(version=None):
    """ Aggregate function to deploy the app. """
    if version is None:
        version = env.version

    stop_webserver()
    kill_uwsgi()
    remove_tmp_files()
    checkout_version(version)
    restart_uwsgi()
    restart_webserver()


def pynt(cmd):
    """ Run a pynt command on the remote host. """
    with virtualenv(env.venv):
        with cd(env.directory):
            run('pynt %s' % cmd)
