from traitlets import HasTraits

_INTERVAL_TYPES = ('minutely', '5 minutes', '10 minutes', '30 minutes', 'hourly', '2 hours', '3 hours', '6 hours', '12 hours', 'daily', 'weekly', 'monthly')
# _REPORT_TYPES = ('convert', 'publish')  # Temporarily disable
_REPORT_TYPES = ('convert',)
_OUTPUT_TYPES = ('notebook', 'pdf', 'html', 'email', 'script')
_PRIVACY_LEVELS = ('public', 'private')
_SERVICE_LEVELS = ('production', 'research', 'development', 'personal')


class Base(HasTraits):
    '''Base HasTraits abstract base class for all paperboy configureables (User, Notebook, Job, and Report)'''

    def __init__(self, config, *args, **kwargs):
        super(Base, self).__init__(*args, **kwargs)
        self.config = config

    @staticmethod
    def from_json(jsn, config):
        '''create a paperboy config object from a json

        Args:
            jsn: python dictionary from json representing the configuration object
            config: paperboy configuration to populate from json

        Returns:
            subclass of Base populated from jsn
        '''
        raise NotImplementedError()

    def to_json(self, include_notebook=False):
        '''convert a paperboy config to a json

        Args:
            self: subclass of Base
            include_notebook: if config would include a notebook (potentially several MB in size), should
                we include it or strip it?

        Returns:
            dict: python dictionary representing the response json
        '''
        raise NotImplementedError()

    def form(self):
        '''generate a JSON form template for the subclass of Base

        Args:
            self: subclass of Base

        Returns:
            dict: python dictionary representing the form template as a JSON
        '''
        raise NotImplementedError()

    def edit(self):
        '''generate a JSON edit template for the subclass of Base

        Args:
            self: subclass of Base

        Returns:
            dict: python dictionary representing the edit template as a JSON
        '''
        raise NotImplementedError()

    def entry(self):
        raise NotImplementedError()

    def store(self):
        raise NotImplementedError()
