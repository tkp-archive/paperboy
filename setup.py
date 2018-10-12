from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    requires = f.read().split()

setup(
    name='paperboy',
    version='0.0.1',
    description='Jupyter notebooks',
    long_description=long_description,
    url='https://github.com/timkpaine/paperboy',
    download_url='https://github.com/timkpaine/paperboy/archive/v0.0.1.tar.gz',
    author='Tim Paine',
    author_email='timothy.k.paine@gmail.com',
    license='BSD 3 Clause',
    install_requires=requires,

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],

    keywords='juyter notebooks jupyterlab analytics',
    zip_safe=False,
    packages=find_packages(exclude=[]),
    include_package_data=True,

    entry_points={
        'console_scripts': [
        ],
    },
)
