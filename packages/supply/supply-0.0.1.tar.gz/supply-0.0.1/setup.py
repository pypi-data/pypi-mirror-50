import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="supply",
    version="0.0.1",
    author="Zefu (Shawn) Lu",
    author_email="shawnlu25@gmail.com",
    description="Supply kit for natural language processing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/shawnlu25/supply",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)