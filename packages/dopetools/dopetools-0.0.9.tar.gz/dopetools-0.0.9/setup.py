from setuptools import setup
import os

if os.environ.get('CI_COMMIT_TAG'):
    version = os.environ['CI_COMMIT_TAG']
else:
    version = '0.0.0'
print(version)

setup(
    name='dopetools',
    version=version,
    description='Useful tools for the DOPE project.',
    author='Badruu',
    author_email='badrus@propulsionacademy.com',
    license='MIT',
    packages=['dopetools'],
    zip_safe=False
)
