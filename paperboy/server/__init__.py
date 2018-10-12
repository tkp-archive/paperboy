from .api import FalconAPI
from .deploy import FalconGunicorn


def main():
    options = {
        'bind': '0.0.0.0:8080',
        'workers': 2
    }
    FalconGunicorn(FalconAPI(), options).run()
