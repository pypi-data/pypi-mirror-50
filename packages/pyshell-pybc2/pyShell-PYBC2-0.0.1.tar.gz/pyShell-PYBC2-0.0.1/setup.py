import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyShell-PYBC2",
    version="0.0.1",
    author="PYBC_2",
    author_email="mmothuku@adobe.com",
    description="A small example package",
    long_description=long_description,
    url="https://git.corp.adobe.com/hsampath/PyShell",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)