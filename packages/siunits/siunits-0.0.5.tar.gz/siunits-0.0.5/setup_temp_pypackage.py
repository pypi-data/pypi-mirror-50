import setuptools
 
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="siunits",
    version="0.0.5",
    author="",
    author_email="",
    description="Perform operations on SI units",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[],
)
