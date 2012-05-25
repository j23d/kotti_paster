import sys
import os
import pkg_resources
import shutil
import subprocess
import tempfile
import time
import httplib


class TemplateTest(object):

    def kotti_addon(self, tmpl_name='kotti_addon', project='werkpalast'):  # pragma: no cover
        try:
            self.old_cwd = os.getcwd()
            self.directory = tempfile.mkdtemp()
            os.chdir(self.directory)
            self.home = pkg_resources.get_distribution('kotti_paster').location
            # create package
            subprocess.check_call(['%s/bin/paster' % self.home, 'create', '-t', tmpl_name, project, '--no-interactive'])
            # create a pytest runner for it via buildout
            cfg = open(os.path.join(project, 'testing.cfg'), 'w')
            cfg.writelines("""
[buildout]
parts =
    pytest
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
            subprocess.check_call([os.path.join(self.home, 'bin', 'buildout'), '-c', 'testing.cfg'])
            # run the tests:
            py_test = os.path.join(self.directory, project, 'bin', 'test')
            proc = subprocess.Popen([py_test, ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = proc.stdout.read()
            if not '100%' in output:
                raise AssertionError
            proc.terminate()
        finally:
            shutil.rmtree(self.directory)
            os.chdir(self.old_cwd)

    def kotti_project(self, tmpl_name='kotti_project'):  # pragma: no cover
        try:
            self.old_cwd = os.getcwd()
            self.directory = tempfile.mkdtemp()
            self.make_venv(self.directory)
            os.chdir(pkg_resources.get_distribution('kotti_paster').location)
            subprocess.check_call(
                [os.path.join(self.directory, 'bin', 'python'),
                 'setup.py', 'dev'])
            os.chdir(self.directory)
            subprocess.check_call(['bin/paster', 'create', '-t', tmpl_name, 'test', '--no-interactive', 'author=johndoe', 'author_email=john@doe.org'])
            py = os.path.join(self.directory, 'bin', 'python')
            os.chdir('test')
            subprocess.check_call([py, 'bootstrap.py'])
            subprocess.check_call(['bin/buildout'])
            pserve = os.path.join(self.directory, 'test', 'bin', 'pserve')
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
        finally:
            shutil.rmtree(self.directory)
            os.chdir(self.old_cwd)


def test_paster_templates():
    test = TemplateTest()
    test.kotti_addon()
    # test.kotti_project()
