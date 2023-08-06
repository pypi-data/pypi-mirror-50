import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py_schema",
    version="0.12.0",
    author="Ben-hur Santos Ott",
    author_email="ben-hur@outlook.com",
    description="A simple and extensible schema validator.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/benhurott/py_schema",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
