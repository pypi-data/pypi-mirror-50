import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="versionchecker",
    version="1.0.0",
    author="Vimal",
    author_email="usvimal@gmail.com",
    description="Check for outdated packages installed on your system and get the latest version number",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/usvimal/versionchecker",
    download_url='https://github.com/usvimal/versionchecker/archive/1.0.0.tar.gz',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
