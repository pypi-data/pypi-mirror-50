import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PytopiaAPI",
    version="1.0.4",
    author="Dest0re",
    author_email="tihokaenglichman@gmail.com",
    description="A python API for Utopia Ecosystem",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Dest0re/PytopiaAPI",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
)