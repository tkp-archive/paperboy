import os
from setuptools import setup, find_packages
from codecs import open
from os import path
from jupyter_packaging import (
    ensure_python, get_version
)

ensure_python(('2.7', '>=3.7'))
pjoin = path.join
name = 'jupyter_paperboy'
here = path.abspath(path.dirname(__file__))
version = get_version(pjoin(here, 'paperboy', '_version.py'))


print('WARNING: https://issues.apache.org/jira/browse/AIRFLOW-1430?subTaskView=unresolved')
os.environ['AIRFLOW_GPL_UNIDECODE'] = '1'

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

requires = [
    'falcon==1.4.1',
    'gitpython>=2.1.11',
    'Jinja2>=2.8.1',
    'nbconvert>=5.4.0',
    'nbformat>=4.4.0',
    'nbstripout>=0.3.3',
    'papermill>=0.16.2',
    'python-crontab>=2.3.8',
    'PyJWT>=1.6.4',
    'traitlets>=4.3.2',
    'sqlalchemy>=1.2.0',
    'voila>=0.0.6',
]

if os.name == 'nt':
    requires.append('waitress')
else:
    requires.append('gunicorn>=19.9.0')

requires_dev = [
    'apache-airflow',
    'codecov',
    'flake8',
    'luigi',
    'matplotlib',
    'mock',
    'pyEX',
    'pytest',
    'pytest-cov',
    'pytest-falcon',
    'pytest-tornasync',
    'python-crontab',
    'pylint',
    'pandas',
    'seaborn',
    'sphinx',
    'sphinx_rtd_theme',
]


setup(
    name=name,
    version=version,
    description='Jupyter notebooks',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/timkpaine/paperboy',
    author='Tim Paine',
    author_email='timothy.k.paine@gmail.com',
    license='BSD 3 Clause',
    python_requires='>=3.5',
    install_requires=requires,
    extras_require={'dev': requires_dev},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
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
            'paperboy = paperboy.server:main',
            'paperboy-worker = paperboy.worker:main'
        ],
    },
)
