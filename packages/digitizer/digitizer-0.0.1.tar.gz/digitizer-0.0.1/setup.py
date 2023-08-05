import setuptools

setuptools.setup(
    name="digitizer",
    version="0.0.1",
    author="William Wyatt",
    author_email="wwyatt@ucsc.edu",
    description="Paser for the caen DT5742",
    long_description="Paser for the caen DT5742",
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    url="https://github.com/Tsangares/",
    include_package_data=True,
    scripts=[
        'numpy>=1.17.0',
    ],
    install_requires=[
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
