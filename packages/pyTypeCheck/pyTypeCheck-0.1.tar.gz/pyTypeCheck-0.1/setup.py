import setuptools
from setuptools import find_packages

setuptools.setup(
  name = 'pyTypeCheck',
  version = '0.1',
  author = 'Giacomo Giusti',
  packages = find_packages(exclude=('test', 'test.*')),
  long_description_content_type='text/markdown', 
  license = 'MIT',
  long_description = open('README.md').read(),
  python_requires='>=3.0.*, <4',
)