import os
from setuptools import setup

setup(
    name = "cseprint",
    version = "1.0.2",
    author = "Daniel Marchese",
    author_email = "marchese.29@osu.edu",
    description = "A utility for printing files to printers on stdlinux.",
    license = "MIT",
    keywords = "ohio state cse print printer",
    packages=['cseprint'],
    entry_points = {
        'console_scripts': [
            'cseprint=cseprint.print:main',
            'cselpstat=cseprint.list:main'
        ]
    },
    classifiers=[
        "Topic :: Utilities"
    ],
)