from setuptools import setup, find_packages
from os import path

from io import open

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='TestDjangoPackage',
    version='1.1.6',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/KathurimaKimathi/testdjangopackage/',
    author='Kathurima Kimathi',
    author_email='kathurima@healthcloud.co.ke',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='sample testdjangopackage setuptools development',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, <4',
    install_requires=['peppercorn', 'django', 'twine', 'sentry-sdk==0.10.1'],
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },
    package_data={
        'TestDjangoPackage': ['*.dat'],
    },
    scripts=['runtestblog'],
)
