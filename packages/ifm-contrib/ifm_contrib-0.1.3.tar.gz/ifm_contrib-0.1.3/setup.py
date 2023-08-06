import setuptools

with open("./ifm_contrib/README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ifm_contrib",
    version="0.1.3",
    author="Alexander Renz",
    author_email="are@dhigroup.com",
    description="Extension for the FEFLOW Python API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dhi/ifm_contrib",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
		"Development Status :: 4 - Beta"
    ],
)