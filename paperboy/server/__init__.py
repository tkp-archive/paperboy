import os
from .api import FalconAPI
from .deploy import FalconGunicorn


def main():
    options = {
        'bind': '0.0.0.0:{}'.format(os.environ.get('PORT', '8080')),
        'workers': 2
    }
    FalconGunicorn(FalconAPI(), options).run()
