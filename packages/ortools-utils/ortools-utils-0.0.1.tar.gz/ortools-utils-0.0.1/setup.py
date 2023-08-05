import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ortools-utils",
    version="0.0.1",
    author="Xiang Chen",
    author_email="xiangchenchen96@gmail.com",
    description="Python utilities for ortools",
    python_requires='>=3.6',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/stradivari96/or-tools-utils",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)