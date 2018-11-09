import os
import os.path
from traitlets import HasTraits, Unicode


class Output(HasTraits):
    type = Unicode()
    pass


class LocalOutput(Output):
    type = 'local'
    dir = Unicode(default_value=os.path.expanduser('~/Downloads'))
