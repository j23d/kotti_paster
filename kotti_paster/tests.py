import os
import subprocess
import httplib
from kotti_paster.conftest import paster


@paster('kotti_addon', 'werkpalast', '--no-interactive')
def test_kotti_addon(pasterdir, pytest_runner):
    tempdir, cwd, project = pasterdir
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
