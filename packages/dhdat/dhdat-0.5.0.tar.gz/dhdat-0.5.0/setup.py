import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(name="dhdat",
  version="0.5.0",
  description="DHDAT is a python package with basic tools to produce interaction matrices and calculate several dominance hierarchy related metrics",
  long_description=README,
  long_description_content_type="text/markdown",
  classifiers=[
    "Development Status :: 4 - Beta",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.7",
    "Topic :: Scientific/Engineering :: Bio-Informatics",
  ],
  url="https://github.com/esvanhaeringen/DHDAT",
  author="Erik van Haeringen",
  author_email="e.s.van.haeringen@student.rug.nl",
  license="MIT",
  packages=["dhdat"],
  install_requires=["pandas"],
  zip_safe=True,
  include_package_data=True)
