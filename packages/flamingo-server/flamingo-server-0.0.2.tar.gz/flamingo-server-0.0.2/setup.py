import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "flamingo-server",
    version = "0.0.2",
    author = "Uncertainty.",
    author_email = "tk@uncertainty.cc",
    description = "A lightweight customizable socket server.",
    long_description=long_description,
    long_description_content_type = "text/markdown",
    url = "",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
