from setuptools import setup

def readme_file_contents():
    with open("Readme.md") as fd:
        return fd.read()

setup(
    name="pygameoflife_dadeerh",
    version="1.0.0",
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