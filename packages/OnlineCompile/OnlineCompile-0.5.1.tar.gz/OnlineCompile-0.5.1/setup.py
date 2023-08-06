import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="OnlineCompile",
    version="0.5.1",
    author="Will F",
    author_email="forsbergw82@gmail.com",
    description="A Python package for running python scripts from the internet",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['Online'],
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)
