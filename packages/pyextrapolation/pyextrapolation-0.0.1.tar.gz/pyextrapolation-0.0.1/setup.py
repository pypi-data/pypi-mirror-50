from setuptools import setup, find_packages
from codecs import open
from os import path

__version__ = '0.0.1'

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pyextrapolation',
    version=__version__,
    description='A python package for multidimensional extrapolation via the solution of a partial differential equation',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/murraycutforth/pyextrapolation',
    download_url='https://github.com/murraycutforth/pyextrapolation/tarball/' + __version__,
    license='BSD',
    classifiers=[
      'Development Status :: 3 - Alpha',
      'Intended Audience :: Developers',
      'Programming Language :: Python :: 3',
    ],
    keywords='',
    packages=find_packages(exclude=['docs', 'tests*']),
    include_package_data=True,
    author='Murray Cutforth',
    install_requires=['numpy>=1.11.0'],
    dependency_links=[],
    author_email='murray.cutforth@eu.medical.canon'
)
