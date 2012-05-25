import os
import subprocess
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


@paster('kotti_project', 'werkpalast', '--no-interactive')
def test_kotti_project(pasterdir, application):
    tempdir, cwd, project = pasterdir
    conn = httplib.HTTPConnection(application)
    conn.request('GET', '/')
    resp = conn.getresponse()
    assert resp.status == 200
    data = resp.read()
    toolbarchunk = b'<div id="pDebug"'
    assert toolbarchunk in data
