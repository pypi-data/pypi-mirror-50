import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kerneloose",
    version="0.0.1",
    author="Andreas Hinterreiter",
    author_email="andreas.hinterreiter@jku.at",
    description="Kernel method for out-of-sample extension",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/einbandi/kerneloose",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)