import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python-lang",
    version="1.0.0",
    author="Grzegorz Babiarz",
    author_email="programista3@outlook.com",
    description="A simple library for building multilingual applications in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Programista3/python-lang",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)