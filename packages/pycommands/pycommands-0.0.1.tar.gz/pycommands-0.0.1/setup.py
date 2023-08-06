import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="pycommands",
    version="0.0.1",
    author_email="rafa.cassau@gmail.com",
    description="Pycommands help you to build system remote call commands",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rafaelcassau/pycommands",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
