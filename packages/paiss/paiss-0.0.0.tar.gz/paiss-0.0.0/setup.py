import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="paiss",
    version="0.0.0",
    author="kenbliky",
    author_email="leebenw@126.com",
    description="Paiss is a library for efficient similarity search for pictures",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kenblikylee/paiss",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
