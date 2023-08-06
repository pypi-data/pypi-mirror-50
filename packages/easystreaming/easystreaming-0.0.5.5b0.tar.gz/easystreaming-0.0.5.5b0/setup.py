import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="easystreaming",
    version="0.0.5.5b",
    author="Jakob Kirsch",
    author_email="jakob.kirsch@teckids.org",
    description="A small Server and Client creator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://edugit.org/jakobkir/simplestreaming",
    packages=["easystreaming"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
