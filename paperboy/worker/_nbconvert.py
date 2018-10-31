import os
import os.path
import subprocess
import sys
try:
    from tempfile import TemporaryDirectory
except ImportError:
    from backports.tempfile import TemporaryDirectory


def run(nb_name, nb_text, to='html', template=''):
    with TemporaryDirectory() as tempdir:

        in_file = os.path.join(tempdir, '{}.ipynb'.format(nb_name))

        out_file = os.path.join(tempdir, '{}_out'.format(nb_name))

        # hack for pdfs, .pdf appended automatically by xelatex
        if to != 'pdf':
            out_file += '.' + to

        with open(in_file, 'wb') as fp:
            fp.write(nb_text)

        # assemble nbconvert command
        argv = []
        argv = [sys.executable, '-m', 'nbconvert', '--to', to]

        # pass in template arg
        if template:
            argv.extend(['--template', template])

        # output to outname
        argv.extend([in_file, '--output', out_file])

        subprocess.call(argv)

        # hack for pdfs
        if to == 'pdf':
            out_file += '.' + to

        with open(out_file, 'rb') as fp:
            ret = fp.read()
    return ret
