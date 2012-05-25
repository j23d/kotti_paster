import os
import pkg_resources
import shutil
import subprocess
import tempfile
from py.test import mark
from mr.laforge import up, waitforports, shutdown

paster = mark.paster

home = pkg_resources.get_distribution('kotti_paster').location


def pytest_funcarg__pasterdir(request):

    def setup():
        directory = tempfile.mkdtemp()
        os.chdir(directory)
        template_name, project_name, extra_parameters = request.keywords['paster'].args
        params = [os.path.join(home, 'bin', 'paster'), 'create', '-t', template_name, project_name]
        params.extend(extra_parameters.split(' '))
        subprocess.check_call(params)
        os.chdir(project_name)
        return (directory,
            os.path.join(directory, project_name),
            project_name)

    def teardown(directory):
        shutil.rmtree(directory[0])

    return request.cached_setup(setup=setup,
        teardown=teardown,
        scope='function')


def pytest_funcarg__application(request):

    def setup():
        tempdir, cwd, project = request._funcargs['pasterdir']
        cfg = open(os.path.join(cwd, 'supervisor.cfg'), 'w')
        cfg.writelines("""
[buildout]
extends = buildout.cfg
parts += supervisor

[supervisor]
recipe = collective.recipe.supervisor
supervisord-conf=${buildout:directory}/supervisord.conf
programs =
    10 app %(cwd)s/bin/pserve [%(cwd)s/development.ini]
""" % dict(cwd=cwd))
        cfg.close()
        subprocess.check_call([os.path.join(home, 'bin', 'buildout'), '-c', 'supervisor.cfg'])
        up('app')
        waitforports(6543)
        return u'localhost:6543'

    def teardown(application):
        shutdown()

    return request.cached_setup(setup=setup,
        teardown=teardown,
        scope='function')
