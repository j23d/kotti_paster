import os
from setuptools import setup, find_packages

install_requires = [
    'setuptools',
    'PasteScript',
    'Cheetah',
    'templer.core',
    ]

tests_require = [
    'virtualenv',
    'PasteScript',
    'Cheetah',
    'pytest',
    'mr.laforge',
    ]

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

setup(name='kotti_paster',
      version='0.1',
      description="Paster AddOn Template for Kotti",
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Buildout",
        "License :: Repoze Public License",
        ],
      keywords='kotti addon scaffold',
      author='Marco Scheidhuber and Tom Lazar',
      author_email='j23d@jusid.de',
      url='http://pypi.python.org/pypi/kotti_paster/',
      license='BSD-derived (http://www.repoze.org/LICENSE.txt)',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      tests_require=tests_require,
      entry_points="""
            [paste.paster_create_template]
            kotti_addon = kotti_paster.paster_templates:Addon
            kotti_project = kotti_paster.paster_templates:Buildout
      """,
      extras_require={
          'testing': tests_require,
          },
      message_extractors={'kotti_paster': [
            ('**.py', 'lingua_python', None),
            ('**.zcml', 'lingua_xml', None),
            ('**.pt', 'lingua_xml', None),
            ]},
      )
