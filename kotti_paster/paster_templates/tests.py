import os
import pkg_resources
import subprocess
import time
import httplib

home = pkg_resources.get_distribution('kotti_paster').location


def test_kotti_addon(tempdir):
    tmpl_name = 'kotti_addon'
    project = 'werkpalast'
    # create package
    subprocess.check_call(['%s/bin/paster' % home, 'create', '-t', tmpl_name, project, '--no-interactive'])
    # create a pytest runner for it via buildout
    cfg = open(os.path.join(project, 'testing.cfg'), 'w')
    cfg.writelines("""[buildout]
parts = pytest
develop = .

[pytest]
recipe = z3c.recipe.scripts
scripts = py.test=test
eggs =
    %s [testing]
    pytest
    """ % project)
    cfg.close()
    os.chdir(project)
    subprocess.check_call([os.path.join(home, 'bin', 'buildout'), '-c', 'testing.cfg'])
    # run the tests:
    py_test = os.path.join(tempdir, project, 'bin', 'test')
    proc = subprocess.Popen([py_test, ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = proc.stdout.read()
    if not '100%' in output:
        raise AssertionError
    proc.terminate()


def kotti_project(tempdir):
    tmpl_name = 'kotti_project'
    os.chdir(pkg_resources.get_distribution('kotti_paster').location)
    subprocess.check_call(
        [os.path.join(tempdir, 'bin', 'python'),
         'setup.py', 'dev'])
    os.chdir(tempdir)
    subprocess.check_call(['bin/paster', 'create', '-t', tmpl_name, 'test', '--no-interactive', 'author=johndoe', 'author_email=john@doe.org'])
    py = os.path.join(tempdir, 'bin', 'python')
    os.chdir('test')
    subprocess.check_call([py, 'bootstrap.py'])
    subprocess.check_call(['bin/buildout'])
    pserve = os.path.join(tempdir, 'test', 'bin', 'pserve')
    ininame = 'development.ini'
    proc = subprocess.Popen([pserve, ininame])
    try:
        time.sleep(5)
        proc.poll()
        if proc.returncode is not None:
            raise RuntimeError('%s didnt start' % ininame)
        conn = httplib.HTTPConnection('localhost:6543')
        conn.request('GET', '/')
        resp = conn.getresponse()
        assert resp.status == 200, ininame
        data = resp.read()
        toolbarchunk = b'<div id="pDebug"'
        assert toolbarchunk in data, ininame
    finally:
        proc.terminate()
