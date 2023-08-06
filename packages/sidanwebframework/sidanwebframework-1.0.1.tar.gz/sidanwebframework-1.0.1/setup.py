import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sidanwebframework",
    version="1.0.1",
    author="sidan",
    description="sidanwebframework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['sidanwebframework'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
