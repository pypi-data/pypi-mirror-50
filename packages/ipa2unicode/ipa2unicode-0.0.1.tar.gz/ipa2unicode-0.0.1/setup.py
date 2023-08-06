import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ipa2unicode",
    version="0.0.1",
    author="Brooke Cowan",
    author_email="cowanb@ohsu.edu",
    description="Package for converting SIL IPA93 legacy font to unicode",
    long_description=long_description,
    long_description_content_type="text/markdown",
    #url="https://github.com/pypa/sampleproject", ## Where should this live?
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
