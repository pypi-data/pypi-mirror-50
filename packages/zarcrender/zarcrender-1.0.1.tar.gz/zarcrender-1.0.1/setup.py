import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zarcrender",
    version="1.0.1",
    author="Fuad Ar-Radhi",
    author_email="fuad.arradhi@gmail.com",
    description="Python JSON serverside render for any JS datagrid library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fuadarradhi/zarcrender",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
