import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="my_pypi_package",
    version="0.0.2",
    author="Mohammadali",
    author_email="mforouzesh@mpi-sws.org",
    description="my First Package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/frzmohammadali/my_pypi_package",
    packages=setuptools.find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=[
        'numpy>=1.17.0',
        'requests>=2.22.0'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
