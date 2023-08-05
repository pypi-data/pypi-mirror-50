import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="WhPy",
    version="0.0.2",
    author="Michael duBois",
    author_email="mdubois@mcduboiswebservices.com",
    description="A Python 3 webhook module.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MichaelCduBois/WhPy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 1 - Planning"
    ]
)
