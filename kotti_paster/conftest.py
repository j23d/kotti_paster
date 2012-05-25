import os
import pkg_resources
import shutil
import subprocess
import tempfile
from py.test import mark

paster = mark.paster

home = pkg_resources.get_distribution('kotti_paster').location


def pytest_funcarg__pasterdir(request):

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
