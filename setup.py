# setup.py
from setuptools import setup

setup(
    name="phi-detection-webhook",
    version="1.0.0",
    py_modules=["regex_check"],
    entry_points={
        "console_scripts": [
            "regex_check = regex_check:main",  # main() function in regex_check.py
        ],
    },
)
