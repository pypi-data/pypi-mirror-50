import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyshell-pybc2-new",
    version="0.0.2",
    author="PYBC_2",
    author_email="lakshmip@adobe.com",
    description="This Package contains the commands of UNIX shell",
    long_description=long_description,
    packages=["pyShell"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)