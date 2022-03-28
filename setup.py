"""atomic6ghg package configuration"""
import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(name="atomic6ghg",
      version="1.0.0",
      description="Library of formulas, conversion factors and schemas for greenhouse gas calculations",
      long_description=README,
      long_description_content_type="text/markdown",
      url="https://github.com/GE-Atomic6/ghg",
      author_email="atomic.6@ge.com",
      author="General Electric Company",
      license="BSD 3-Clause License",
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "License :: OSI Approved :: BSD License",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.10",
      ],
      packages=["atomic6ghg", "atomic6ghg.factors", "atomic6ghg.formulas", "atomic6ghg.schemas"],
      package_data={
          'atomic6ghg': ['schemas/*.json',
                         'factors/source_data/*.json',
                         'formulas/*.json'],
      },
      install_requires=[]
      )
