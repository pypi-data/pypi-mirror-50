from setuptools import setup
import os


version = '0.1.1'

setup(
    name='dopetools',
    version=version,
    description='Useful tools for the DOPE project.',
    author='Badruu',
    author_email='badrus@propulsionacademy.com',
    license='MIT',
    packages=['dopetools'],
    install_requires=['pandas'],
    zip_safe=False
)
