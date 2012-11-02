import os
import pkg_resources
import shutil
import subprocess
import tempfile

from mr.laforge import shutdown
from mr.laforge import up
from mr.laforge import waitforports
from py.test import mark

paster = mark.paster
home = pkg_resources.get_distribution('kotti_paster').location


def pytest_funcarg__pasterdir(request):
    """ Creates a temporary directory, changes into it and runs ``paster create`` in it
    using the template name, project name and any additional parameters passed in via
    the ``paster`` marker.

    The return value is a tuple of the full path of the temporary directory, the full
    path to the directory created by the temporary directory and the name of the project.

    E.g. the following marker would call ``paster create -t foo bar --no-interactive``::

        @paster('foo', 'bar', '--no-interactive')
        def test_foo_bar(pasterdir):
            assert 'foo.txt' in os.listdir(pasterdir)

    The teardown method deletes the temporary directory again.
    """

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
    """ Assuming that ``pytest_funcarg__pasterdir`` has run and created a directory containing a ``buildout.cfg``
    and a ``development.ini`` that configures an application on port 6543, runs that buildout
    and starts the application via supervisor.

    On teardown supervisord is shut down.
    """
    def setup():
        tempdir, cwd, project = request._funcargs['pasterdir']
        cfg = open(os.path.join(cwd, 'supervisor.cfg'), 'w')
        cfg.writelines("""
[buildout]
extends = buildout.cfg
parts += supervisor

find-links = http://cheeseshop.jusid.de/cheeseshop/catalog/simple

versions = versions

[versions]
Kotti = 0.8.0dev

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


def pytest_funcarg__pytest_runner(request):
    """ Assuming that ``pytest_funcarg__pasterdir`` has run, creates and runs a testrunner for its egg.

    Return value is an instance of ``subprocess.Popen`` running the tests.

    Teardown terminates that process.
    """
    def setup():
        # create a pytest runner via buildout
        tempdir, cwd, project = request._funcargs['pasterdir']
        cfg = open(os.path.join(cwd, 'testing.cfg'), 'w')
        cfg.writelines("""[buildout]
parts = pytest
develop = .

find-links = http://cheeseshop.jusid.de/cheeseshop/catalog/simple

versions = versions

[versions]
Kotti = 0.8.0dev

[pytest]
recipe = z3c.recipe.scripts
scripts = py.test=test
eggs =
    Kotti
    %s [testing]
    pytest
        """ % project)
        cfg.close()
        subprocess.check_call([os.path.join(home, 'bin', 'buildout'), '-c', 'testing.cfg'])
        # run the tests:
        return subprocess.Popen([os.path.join(cwd, 'bin', 'test')],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

    def teardown(pytest_runner):
        pytest_runner.terminate()

    return request.cached_setup(setup=setup,
        teardown=teardown,
        scope='function')
