"""
Build module for myonotify library
"""
from setuptools import setup

REQUIREMENTS = [
    'boto3',
]

setup(
    name='myonotify',
    version='1.0',
    description='',
    python_requires='>3.6',
    url='https://github.com/',
    author='MJ Krakowski',
    author_email='mj.krakowski@myoptiquegroup.com',
    packages=['myonotify'],
    install_requires=REQUIREMENTS,
    zip_safe=True,
)
