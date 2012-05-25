import os
import pkg_resources
import subprocess
import time
import httplib

from kotti_paster.conftest import paster, home


@paster('kotti_addon', 'werkpalast', '--no-interactive')
def test_kotti_addon(pasterdir):
    tempdir, cwd, project = pasterdir
    # create a pytest runner for it via buildout
    cfg = open(os.path.join(cwd, 'testing.cfg'), 'w')
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
    subprocess.check_call([os.path.join(home, 'bin', 'buildout'), '-c', 'testing.cfg'])
    # run the tests:
    proc = subprocess.Popen([os.path.join(cwd, 'bin', 'test')],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    output = proc.stdout.read()
    assert '100%' in output
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
