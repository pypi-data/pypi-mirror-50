from setuptools import setup

with open("README.md") as f:
    long_description = f.read()

setup(
    name="cipher_tools",
    version="0.0.2",
    url="https://gitlab.com/lukespademan/cipher-tools",
    author="Luke Spademan",
    author_email="info@lukespademan.com",
    description="A python library to assist in the creation of ciphers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=["cipher_tools"],
    package_dir={"": "src"},
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
)
