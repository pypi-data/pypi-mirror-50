import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="unix-pyshell-pybc2",
    version="0.0.1",
    author="PYBC_2",
    author_email="mmothuku@adobe.com",
    description="This Package contains the commands of UNIX shell",
    long_description=long_description,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)