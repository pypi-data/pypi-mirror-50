import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name='TermIO',
    version='0.1.6',
    scripts=[],
    author="jakobst1n",
    author_email="jakob.stendahl@outlook.com",
    description="Simple terminal manipulator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jakobst1n/TermIO-python-package",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
