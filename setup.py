from setuptools import setup, find_packages
import sys, os

version = '0.1'

install_requires = [
    'pyramid>=1.3',
    'Paste',
    ]

tests_require = [
    'WebTest',
    'mock',
    'pytest',
    'pytest-cov',
    'pytest-xdist',
    'wsgi_intercept',
    'zope.testbrowser',
    ]

setup(name='kotti_paster',
      version=version,
      description="Paster AddOn Template for Kotti",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='kotti addon scaffold',
      author='j23d',
      author_email='j23d@jusid.de',
      url='jusid.de',
      license='GPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      tests_require=tests_require,
      entry_points="""
            [pyramid.scaffold]
            kotti_paster = kotti_paster.paster_templates:KottiAddonTemplate
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
