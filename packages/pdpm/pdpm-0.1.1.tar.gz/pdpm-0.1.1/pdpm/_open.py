import os
import pickle


def _open() -> str:
    with open(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'path.pickle'), 'rb') as f:
        return pickle.load(f)


def _open_launcher() -> str:
    with open(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'launcher.pickle'), 'rb') as f:
        return pickle.load(f)
