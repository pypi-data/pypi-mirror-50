import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="scriptoria",
    version="0.0.2",
    author="Sean Bethard",
    author_email="sean@seanbethard.com",
    description="Aufschreibesystem 2000",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/seancska/corpuswork/scriptoria",
    packages=setuptools.find_packages(),
    license="License :: OSI Approved :: Apache Software License"
)