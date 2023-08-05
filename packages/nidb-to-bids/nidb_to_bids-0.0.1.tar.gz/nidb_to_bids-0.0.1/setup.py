import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name="nidb_to_bids",
    version="0.0.1",
    author="Dylan Nielson",
    author_email="Dylan.Nielson@gmail.com",
    description="Our lab's code to convert data dumped from NiDB to BIDS",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nimh-mbdu/nidb_to_bids",
    #packages=setuptools.find_packages(),
    packages=['nidb_to_bids'],
    install_requires=[
        'pandas',
        'numpy',
        'nibabel',
        'Click'
    ],
    entry_points='''
        [console_scripts]
        parse_nidb_metadata=nidb_to_bids.parse_nidb_metadata:extract_nidb_metadata
    ''',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
        "Operating System :: POSIX",
    ],
)
