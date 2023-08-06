import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyObjective",
    version="0.1.3",
    author="Devansh Agrawal",
    author_email="devanshinspace@gmail.com",
    description="A tool to allow optimization of complex objects using scipy.optimize",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dev10110/pyObjective",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)