"""atomic6-ghg package configuration"""
import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(name="atomic6-ghg",
      version="0.1.0",
      description="Library of constants, conversion factors and functions for greenhouse gas calculations",
      long_description=README,
      long_description_content_type="text/markdown",
      url="https://github.com/GE-Atomic6/ghg",
      author_email="atomic.6@ge.com",
      author="General Electric Company",
      license="BSD 3-Clause License",
      classifiers=[
          "License :: OSI Approved :: BSD License",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.10",
      ],
      packages=["atomic6-ghg", "atomic6-ghg.factors", "atomic6-ghg.formulas", "atomic6-ghg.schemas"],
      package_data={
          'atomic6-ghg': ['schemas/*.json',
                          'factors/source_data/*.json',
                          'formulas/*.json'],
      },
      install_requires=[],
      # entry_points={
      #     "console_scripts": [
      #         "atomic6-ghg=atomic6-ghg.__main__:main",
      #     ]
      # },
      )
