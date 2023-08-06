import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="simplestpythonpkgever",
    version="0.0.1",
    author="Jonathan",
    description="A small example package",
    long_description_content_type="text/markdown",
    url="https://github.com/jonathan-marsan/simplestpythonpkgever",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
