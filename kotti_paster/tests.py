import os
import httplib
from kotti_paster.conftest import paster


@paster('kotti_addon', 'werkpalast', '--no-interactive')
def test_kotti_addon(pasterdir, pytest_runner):
    tempdir, cwd, project = pasterdir
    output = pytest_runner.stdout.read()
    assert '100%' in output
    pytest_runner.terminate()


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


@paster('kotti_project', 'werkpalast', 'gitignore=yes --no-interactive')
def test_kotti_project_gitignore(pasterdir):
    tempdir, cwd, project = pasterdir
    assert '.gitignore' in os.listdir(cwd)


@paster('kotti_project', 'werkpalast', 'gitignore=no --no-interactive')
def test_kotti_project_no_gitignore(pasterdir):
    tempdir, cwd, project = pasterdir
    assert '.gitignore' not in os.listdir(cwd)
