import os
from setuptools import setup

def readme_file_contents():
    readme_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),"Readme.md")
    with open(readme_path) as fd:
        return fd.read()

setup(
    name="pygameoflife_dadeerh",
    version="1.1.3",
    description="Pygame implementation of Conway's Game of Life",
    long_description= readme_file_contents(),
    url="",
    author="dadeerh",
    author_email="dadeerh91@gmail.com",
    license="GPL-3.0",
    packages=[
        "pygameoflife_dadeerh"
    ],
    scripts=[
        "bin/pygameoflife_dadeerh",
        "bin/pygameoflife_dadeerh.bat"
    ],
    zip_safe=False,
    install_requires=[
        "pygame"
    ]
)