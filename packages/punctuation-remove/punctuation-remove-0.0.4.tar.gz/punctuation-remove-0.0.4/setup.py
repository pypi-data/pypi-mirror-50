import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="punctuation-remove",
    version="0.0.4",
    author="Talha Shaikh",
    author_email="talha.shaikh5@gmail.com",
    description="Punctuation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/talhashaikh5/Punctuation.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
