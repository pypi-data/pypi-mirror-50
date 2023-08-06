import os
import sys
from distutils.util import convert_path

sys.path.append(os.getcwd())

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

main_ = {}
ver_path = convert_path('porespy/__init__.py')
with open(ver_path) as f:
    for line in f:
        if line.startswith('__version__'):
            exec(line, main_)

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name='porespy',
    description='A set of tools for analyzing 3D images of porous materials',
    long_description=long_description,
    # long_description_content_type="text/x-rst",
    version=main_['__version__'],
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: OSI Approved :: MIT License',
                 'Programming Language :: Python',
                 'Topic :: Scientific/Engineering',
                 'Topic :: Scientific/Engineering :: Physics'],
    packages=['porespy',
              'porespy.tools',
              'porespy.generators',
              'porespy.metrics',
              'porespy.filters',
              'porespy.networks',
              'porespy.visualization',
              'porespy.io'],
    install_requires=['numpy',
                      'scipy',
                      'matplotlib',
                      'scikit-image',
                      'pandas',
                      'imageio',
                      'tqdm',
                      'array_split',
                      'pytrax',
                      'pyevtk',
                      'numba',
                      'openpnm'],
    author='Jeff Gostick',
    author_email='jgostick@gmail.com',
    url='http://porespy.org',
    project_urls={
        'Documentation': 'https://porespy.readthedocs.io/en/master/',
        'Source': 'https://github.com/PMEAL/porespy/',
        'Tracker': 'https://github.com/PMEAL/porespy/issues',
    },
)
