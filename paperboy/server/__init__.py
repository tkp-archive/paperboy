import sys


def main():
    from ..config.application import Paperboy
    Paperboy.launch_instance(sys.argv)
