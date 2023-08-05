import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="urban_dictionary_parser_py",
    version="0.1",
    author="Rapciu",
    author_email="mrapczewski711@gmail.com",
    description="A python parser for urban dictionary rest api.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Rapciu/urban-dictionary-rest-api-py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable"
    ],
)
