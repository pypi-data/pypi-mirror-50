import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="resumejson_converter",
    version="0.1",
    author="neodarz",
    author_email="neodarz@neodarz.net",
    description="A small package for convert json resume with templating to html and pdf",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.neodarz.net/neodarz/resumejson_converter.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
    ],
    scripts=['bin/resumejson_converter']
)
