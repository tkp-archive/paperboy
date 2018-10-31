import os
import os.path
import subprocess
from tempfile import NamedTemporaryFile
from venv import create


def create_virtualenv(requirements_txt, directory):
    create(directory, with_pip=True)

    source = os.path.join(directory, 'bin', 'activate')
    with NamedTemporaryFile(suffix='txt') as fp:
        fp.write(requirements_txt.encode('utf-8'))
        command = ['source', source, '&&', 'pip', 'install', '-r', fp.name]
        subprocess.call(command)
