import sys
import os
import pkg_resources
import shutil
import subprocess
import tempfile
import time

try:
    import httplib
except ImportError:  # pragma: no cover
    import http.client as httplib

from pyramid.compat import PY3


class TemplateTest(object):

    def make_venv(self, directory):  # pragma: no cover
        import virtualenv
        import sys
        from virtualenv import Logger
        logger = Logger([(Logger.level_for_integer(2), sys.stdout)])
        virtualenv.logger = logger
        virtualenv.create_environment(directory,
                                      site_packages=False,
                                      clear=False,
                                      unzip_setuptools=True,
                                      use_distribute=PY3)

    def test_kotti_addon(self, tmpl_name='kotti_addon'):  # pragma: no cover
        try:
            self.old_cwd = os.getcwd()
            self.directory = tempfile.mkdtemp()
            self.make_venv(self.directory)
            os.chdir(pkg_resources.get_distribution('kotti_paster').location)
            subprocess.check_call(
                [os.path.join(self.directory, 'bin', 'python'),
                 'setup.py', 'dev'])
            os.chdir(self.directory)
            subprocess.check_call(['bin/paster', 'create', '-t', tmpl_name, 'test', 'author=johndoe', 'author_email=john@doe.org'])
            py = os.path.join(self.directory, 'bin', 'python')
            os.chdir('test')
            subprocess.check_call([py, 'setup.py', 'dev'])
            py_test = os.path.join(self.directory, 'bin', 'py.test')
            proc = subprocess.Popen([py_test, ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = proc.stdout.read()
            if not '100%' in output:
                raise AssertionError
            proc.terminate()
        finally:
            shutil.rmtree(self.directory)
            os.chdir(self.old_cwd)

    def test_kotti_project(self, tmpl_name='kotti_project'):  # pragma: no cover
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
            pserve = os.path.join(self.directory, 'bin', 'pserve')
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

test = TemplateTest()
test.test_kotti_addon()
# test.test_kotti_project()
