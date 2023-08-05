import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mathwords",
    version="0.0.1",
    author="playfulpachyderm",
    author_email="playful.pachyderm@gmail.com",
    description="A calculator that uses words",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/playfulpachyderm/mathwords",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
