import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

setuptools.setup(
    name="extended-webdrivers",
    version='0.5',
    author="Dillon Miller",
    author_email="dillon.miller@act.com",
    description="Extends the functionality of selenium webdriver.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dillonm197/extended-webdrivers",
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=install_requires,
)
