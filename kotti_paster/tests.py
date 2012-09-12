import os
import httplib
from kotti_paster.conftest import paster


@paster('kotti_addon', 'werkpalast', 'content_type=yes --no-interactive')
def test_kotti_addon_content_type(pasterdir, pytest_runner):
    output = pytest_runner.stdout.read()
    assert 'werkpalast/tests/test_browser_minimal.rst' in output
    assert 'werkpalast/tests/test_functional_content_type' in output
    assert '10 passed' in output
    assert '100%' in output


@paster('kotti_addon', 'werkpalast', 'content_type=no --no-interactive')
def test_kotti_addon_no_content_type(pasterdir, pytest_runner):
    output = pytest_runner.stdout.read()
    assert 'werkpalast/tests/test_browser_minimal.rst' in output
    assert 'werkpalast/tests/test_functional_content_type' not in output
    assert '4 passed' in output
    assert '100%' in output


@paster('kotti_addon', 'werkpalast', '--no-interactive')
def test_kotti_addon_fanstatic(pasterdir):
    tempdir, cwd, project = pasterdir
    setup_file = open('%s/setup.py' % cwd).read()
    search_string = '[fanstatic.libraries]\n      '\
                    '%(project)s = %(project)s:library' % {'project': project}
    assert search_string in setup_file
    assert 'static.py' in os.listdir(cwd + '/' + project)


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


@paster('kotti_project', 'werkpalast', 'omelette=yes --no-interactive')
def test_kotti_project_omelette(pasterdir):
    tempdir, cwd, project = pasterdir
    buildout_file = open('%s/buildout.cfg' % cwd).read()
    assert '[omelette]' in buildout_file
    assert '\n    omelette' in buildout_file


@paster('kotti_project', 'werkpalast', 'omelette=no --no-interactive')
def test_kotti_project_no_omelette(pasterdir):
    tempdir, cwd, project = pasterdir
    buildout_file = open('%s/buildout.cfg' % cwd).read()
    assert '[omelette]' not in buildout_file
    assert '\n    omelette' not in buildout_file


@paster('kotti_project', 'werkpalast', 'codeintel=yes --no-interactive')
def test_kotti_project_codeintel(pasterdir):
    tempdir, cwd, project = pasterdir
    buildout_file = open('%s/buildout.cfg' % cwd).read()
    assert '[codeintel]' in buildout_file
    assert '\n    codeintel' in buildout_file


@paster('kotti_project', 'werkpalast', 'codeintel=no --no-interactive')
def test_kotti_project_no_codeintel(pasterdir):
    tempdir, cwd, project = pasterdir
    buildout_file = open('%s/buildout.cfg' % cwd).read()
    assert '[codeintel]' not in buildout_file
    assert '\n    codeintel' not in buildout_file


@paster('kotti_project', 'werkpalast', 'codeintel=yes omelette=yes --no-interactive')
def test_kotti_project_codeintel_with_omelette(pasterdir):
    tempdir, cwd, project = pasterdir
    buildout_file = open('%s/buildout.cfg' % cwd).read()
    assert '[codeintel]' in buildout_file
    assert '\n    codeintel' in buildout_file


@paster('kotti_project', 'werkpalast', 'codeintel=yes omelette=no --no-interactive')
def test_kotti_project_no_codeintel_without_omelette(pasterdir):
    tempdir, cwd, project = pasterdir
    buildout_file = open('%s/buildout.cfg' % cwd).read()
    assert '[codeintel]' not in buildout_file
    assert '\n    codeintel' not in buildout_file


@paster('kotti_project', 'werkpalast', 'supervisor=yes --no-interactive')
def test_kotti_project_supervisor(pasterdir):
    tempdir, cwd, project = pasterdir
    buildout_file = open('%s/buildout.cfg' % cwd).read()
    assert '[supervisor]' in buildout_file
    assert '\n    supervisor' in buildout_file


@paster('kotti_project', 'werkpalast', 'supervisor=no --no-interactive')
def test_kotti_project_no_supervisor(pasterdir):
    tempdir, cwd, project = pasterdir
    buildout_file = open('%s/buildout.cfg' % cwd).read()
    assert '[supervisor]' not in buildout_file
    assert '\n    supervisor' not in buildout_file
