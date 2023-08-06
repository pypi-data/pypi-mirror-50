from setuptools import find_packages, setup
import os

version = '2.1.5'


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


long_description = (
    read('README.md')
    + '\n' +
    read('CHANGES.md')
    + '\n')

setup(name='pub.tools',
      version=version,
      description="Package of tools for formatting publication data and accessing data from Entrez tool",
      long_description=long_description,
      classifiers=[
          "Framework :: Plone :: 5.0",
          "Framework :: Plone :: 5.1",
          "Programming Language :: Python",
          "Topic :: Scientific/Engineering",
          "Topic :: Scientific/Engineering :: Bio-Informatics",
          "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      keywords='',
      author='Eric Wohnlich',
      author_email='wohnlice@imsweb.com',
      url='http://git.imsweb.com/wohnlice/pub.tools',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['pub'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'biopython>=1.73',
          'unidecode',
          'lxml',
          'requests',
          'six',
          'future'
      ],
      )
