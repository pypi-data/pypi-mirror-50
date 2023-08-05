"""Setup script for realpython-reader"""

import os.path
from setuptools import setup

# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# # The text of the README file
# with open(os.path.join(HERE, "README.md")) as fid:
#     README = fid.read()

# This call to setup() does all the work
setup(
    name="test_package_balobinp",
    version="1.0.0",
    description="Just a teat package",
    # long_description=README,
    # long_description_content_type="text/markdown",
    author="Pavel Balobin",
    author_email="office@realpython.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
    packages=["test_package_balobinp"],
    # include_package_data=True,
    install_requires=[
        "pandas"
    ],
    # entry_points={"console_scripts": ["realpython=reader.__main__:main"]},
)