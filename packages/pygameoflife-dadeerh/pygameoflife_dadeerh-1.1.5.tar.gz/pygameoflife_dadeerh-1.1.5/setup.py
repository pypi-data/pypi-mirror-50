import os
from setuptools import setup

def readme_file_contents():
    readme_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),"Readme.md")
    with open(readme_path) as fd:
        return fd.read()

setup(
    name="pygameoflife_dadeerh",
    version="1.1.5",
    description="Pygame implementation of Conway's Game of Life",
    long_description= readme_file_contents(),
    long_description_content_type='text/markdown',
    url="https://github.com/Dadeerh/pygameoflife_dadeerh",
    author="dadeerh",
    author_email="dadeerh91@gmail.com",
    license="GPL-3.0",
    packages=[
        "pygameoflife_dadeerh"
    ],
    include_package_data=True,
    scripts=[
        "bin/pygameoflife_dadeerh",
        "bin/pygameoflife_dadeerh.bat"
    ],
    zip_safe=False,
    install_requires=[
        "pygame"
    ]
)