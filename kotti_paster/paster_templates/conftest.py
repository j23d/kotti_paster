import os
import shutil
import tempfile


def pytest_funcarg__tempdir(request):

    def setup():
        directory = tempfile.mkdtemp()
        os.chdir(directory)
        return directory

    def teardown(directory):
        shutil.rmtree(directory)

    return request.cached_setup(setup=setup,
        teardown=teardown,
        scope='function')
