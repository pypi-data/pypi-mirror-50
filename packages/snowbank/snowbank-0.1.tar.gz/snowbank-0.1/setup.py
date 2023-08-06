import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="snowbank",
    version="0.1",
    author="Pranoy Dev",
    author_email="devpranoy@gmail.com",
    description="Python Package to integrate lightning network cpapbility",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/syoolah/snowbank",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
