import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="AIOrqlite",
    version="0.1.4",
    author="Terra Brown",
    author_email="superloach42@gmail.com",
    description="Ayncio-based Python client for rqlite.",
    long_description=long_description,
    url="https://github.com/superloach/aiorqlite",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
