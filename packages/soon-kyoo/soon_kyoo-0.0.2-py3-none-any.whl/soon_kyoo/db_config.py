"""Defines configuration for the database.
"""

import pathlib


here = pathlib.Path(__file__)
db_path = here.parents[0] / 'instance' / 'queue.sqlite'
