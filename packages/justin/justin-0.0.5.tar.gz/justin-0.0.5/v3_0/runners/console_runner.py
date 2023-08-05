#! venv/Scripts/python
# https://stackoverflow.com/questions/1934675/how-to-execute-python-scripts-in-windows - in case running will break
from pathlib import Path

from v3_0.runners import general_runner


def run():
    general_runner.run(Path.home())
