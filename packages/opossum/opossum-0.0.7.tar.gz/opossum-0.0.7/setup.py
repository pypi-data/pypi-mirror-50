import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="opossum",
    version="0.0.7",
    author="Tobias Krebs, Julian Winkel",
    author_email="julian.winkel@hu-berlin.de",
    description="Simulated Data Generating Process",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://humboldt-wi.github.io/blog/research/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

