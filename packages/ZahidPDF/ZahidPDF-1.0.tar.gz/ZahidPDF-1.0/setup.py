import setuptools
from pathlib import Path

setuptools.setup(
    name="ZahidPDF",
    version="1.0",
    long_description=Path("README.md").read_text(),
    # NEed to tell setuptools about the 2 modules and packages we are going to publish
    # This method will automatically locate the packages we have defined but we need to exclude
    # test and data because they dont include source code
    packages=setuptools.find_packages(exclude=['tests', 'data'])

)
