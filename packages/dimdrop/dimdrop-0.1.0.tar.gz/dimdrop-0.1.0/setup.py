import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dimdrop",
    version="0.1.0",
    author="Theo Dedeken",
    author_email="theo.dedeken@telenet.be",
    description="Providing some dimensionality reduction methods using Machine Learning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/theodedeken/dimdrop",
    packages=setuptools.find_packages(),
    install_requires=[
        "numpy",
        "keras",
        "sklearn",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
