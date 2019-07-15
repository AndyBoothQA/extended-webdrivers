import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="extended-webdrivers",
    version="0.0.8",
    author="Dillon Miller",
    author_email="dillon.miller@swiftpage.com",
    description="Extends the functionality of selenium webdriver.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dillonm197/extended-webdrivers",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'selenium>=3.141.0',
    ],
    include_package_data=True)
