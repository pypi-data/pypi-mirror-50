import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# Allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(name='lesionprocessor',
      version='0.1.0',
      description='Crops or labels lesion(s) shown in an image.',
      long_description=README,
      url='https://github.com/marsbound/lesion-processor',
      author='Clark Lee',
      author_email='marsbound@pm.me',
      license='Apache License 2.0',
      classifiers=[
          'Programming Language :: Python :: 3.6',
      ],
      packages=find_packages(exclude=['docs', 'tests']),
      python_requires='<=3.6,>=3',
      install_requires=[
          'opencv-python',
          'numpy',
          'tqdm',
          'pathos'
      ],
      test_suite="tests")