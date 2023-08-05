from distutils.core import setup
import setuptools

version = '1.3.20'

packages = ['metagenomi', 'metagenomi/tasks', 'metagenomi/models', 'tests', 'tests/factories', 'tests/models', 'tests/factories/providers', 'hmmdb', 'hmmdb/models', 'metagenomi/parsers', 'metagenomi/scripts']

#scripts = ['metagenomi/helpers.py', 'metagenomi/metadata.py']

classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 3']

requirements = ['boto3', 'pandas', 'cerberus', 'geopy', 'biopython', 'pytest']

setup(
    name='metagenomi',
    author='Metagenomi.co',
    author_email='info@metagenomi.co',
    version=version,
    packages=packages,
    license='MIT',
    long_description=open('README.md').read(),
    install_requires=requirements,
    classifiers=classifiers,
    url='http://metagenomi.co'
)
