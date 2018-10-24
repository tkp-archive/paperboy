from traitlets import HasTraits

_INTERVAL_TYPES = ('minutely', '5 minutes', '10 minutes', '30 minutes', 'hourly', '2 hours', '3 hours', '6 hours', '12 hours', 'daily', 'weekly', 'monthly')
_REPORT_TYPES = ('run', 'publish')
_OUTPUT_TYPES = ('notebook', 'pdf', 'html', 'email', 'script')
_PRIVACY_LEVELS = ('public', 'private')
_SERVICE_LEVELS = ('production', 'research', 'development', 'personal')


class Base(HasTraits):
    def __init__(self, config, *args, **kwargs):
        super(Base, self).__init__(*args, **kwargs)
        self.config = config
