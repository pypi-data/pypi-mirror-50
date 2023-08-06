from os import path
from setuptools import setup

this_dir = path.abspath(path.dirname(__file__))
with open(path.join(this_dir, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="sunscreen",
    version="0.0.3",
    description="What's the UV forecast?",
    author="Jon Miller",
    author_email="jondelmil@gmail.com",
    url="https://github.com/jmillxyz/sunscreen",
    py_modules=["sunscreen"],
    install_requires=["appdirs", "arrow", "colored", "click", "requests"],
    entry_points="""
        [console_scripts]
        sunscreen=sunscreen:main
    """,
    classifiers=(
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
)
