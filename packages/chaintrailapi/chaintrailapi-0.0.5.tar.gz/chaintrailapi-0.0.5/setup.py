import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="chaintrailapi",
    version="0.0.5",
    author="Sebastian Wyngaard",
    author_email="basbot@gmail.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/swyngaard/chaintrailapi",
    packages=setuptools.find_packages(),
    install_requires=['requests-toolbelt'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
