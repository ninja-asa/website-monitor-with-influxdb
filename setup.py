# setup.py
from setuptools import setup, find_packages

requirements = []
# Read requirements from requirements.txt
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='webmonitor',
    version='1.0.0',
    description='A web monitoring service package',
    author='ninja-asa',
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'webmonitor=webmonitor.app:main',
        ],
    },
)
