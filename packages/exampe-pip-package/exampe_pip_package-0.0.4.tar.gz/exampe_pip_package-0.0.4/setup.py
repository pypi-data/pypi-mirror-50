import setuptools

import platform


file_name = "README.md"

if platform.python_version().find("2.7") != -1:
    with open(file_name, "r") as fh:
        long_description = fh.read()
else:
    with open(file_name, "r", encoding='UTF-8') as fh:
        long_description = fh.read()

setuptools.setup(
    name="exampe_pip_package",
    version="0.0.4",
    author="geekpanshi",
    author_email="vincentsxg@gmail.com",
    description="Just a pip package example",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/XingangShi/exampe_pip_package.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

)
