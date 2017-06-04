import os
from setuptools import find_packages
from setuptools import setup
import sys


sys.path.insert(0, os.path.abspath('lib'))

exec(open('lib/ansiblevars/version.py').read())

setup(
    name='ansible-vars',
    version=__version__,
    description=('summarizes variables used in roles'),
    keywords='ansible',
    author='lostbearlabs',
    author_email='eric@lostbearlabs.com',
    url='https://github.com/lostbearlabs/ansible-vars',
    package_dir={'': 'lib'},
    packages=find_packages('lib'),
    zip_safe=False,
    install_requires=['ansible', 'pyyaml', 'six'],
    entry_points={
        'console_scripts': [
             'ansible-vars= ansiblevars.main:main'
        ]
    },
    license='THE UNLICENSE',
    test_suite="test"
)

