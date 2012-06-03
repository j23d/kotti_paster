import os
import httplib
from kotti_paster.conftest import paster


@paster('kotti_addon', 'werkpalast', 'content_type=yes --no-interactive')
def test_kotti_addon_content_type(pasterdir, pytest_runner):
    output = pytest_runner.stdout.read()
    assert 'werkpalast/tests/test_browser_minimal.rst' in output
    assert 'werkpalast/tests/test_functional_content_type' in output
    assert '9 passed' in output
    assert '100%' in output


@paster('kotti_addon', 'werkpalast', 'content_type=no --no-interactive')
def test_kotti_addon_no_content_type(pasterdir, pytest_runner):
    output = pytest_runner.stdout.read()
    assert 'werkpalast/tests/test_browser_minimal.rst' in output
    assert 'werkpalast/tests/test_functional_content_type' not in output
    assert '3 passed' in output
    assert '100%' in output


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


@paster('kotti_project', 'werkpalast', 'travis=yes --no-interactive')
def test_kotti_project_travis(pasterdir):
    tempdir, cwd, project = pasterdir
    assert '.travis.yml' in os.listdir(cwd)


@paster('kotti_project', 'werkpalast', 'travis=no --no-interactive')
def test_kotti_project_no_travis(pasterdir):
    tempdir, cwd, project = pasterdir
    assert '.travis.yml' not in os.listdir(cwd)
