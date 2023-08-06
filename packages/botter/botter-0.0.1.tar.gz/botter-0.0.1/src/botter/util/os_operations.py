import os

def safe_remove(f: str):
    if (os.path.isfile(f)):
        try:
            os.remove(f)
        except OSError:
            pass

__all__ = \
[
    'safe_remove',
]
