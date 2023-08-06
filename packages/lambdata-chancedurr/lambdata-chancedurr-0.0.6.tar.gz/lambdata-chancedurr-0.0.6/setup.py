import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lambdata-chancedurr",
    version="0.0.6",
    author="Chance Dare",
    author_email="chancedurr@gmail.com",
    description="A small helper package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chancedurr",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

