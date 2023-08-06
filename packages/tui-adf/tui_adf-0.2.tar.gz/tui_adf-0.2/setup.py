import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tui_adf",
    version="0.2",
    author="Michael Riesmeyer",
    author_email="Michael.Riesmeyer@tu-ilmenau.de",
    description="Funktionen für Lehrveranstaltung Analoge Digitale Filter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    #url="https://github.com/Kyrioris/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)