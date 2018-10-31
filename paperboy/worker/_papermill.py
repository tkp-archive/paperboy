import os
import os.path
from papermill import execute_notebook
try:
    from tempfile import TemporaryDirectory
except ImportError:
    from backports.tempfile import TemporaryDirectory


# def execute_notebook(
#     input_path,
#     output_path,
#     parameters=None,
#     engine_name=None,
#     prepare_only=False,
#     kernel_name=None,
#     progress_bar=True,
#     log_output=False,
#     start_timeout=60,
#     report_mode=False,
# ):

def run(nb_name, nb_text, parameters, hide_input):
    '''Run the notebook and return the text'''
    with TemporaryDirectory() as tempdir:

        in_file = os.path.join(tempdir, '{}.ipynb'.format(nb_name))
        out_file = os.path.join(tempdir, '{}_out.ipynb'.format(nb_name))

        with open(in_file, 'wb') as fp:
            fp.write(nb_text)

        notebook_object = execute_notebook(in_file, out_file, parameters=parameters, report_mode=hide_input, start_timeout=600)

        with open(out_file, 'rb') as fp:
            output_text = fp.read()

    return output_text, notebook_object
