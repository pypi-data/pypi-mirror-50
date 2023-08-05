import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rafael",
    version="0.0.1",
    author="Rafael",
    author_email="rafa@rayes.com",
    description="Um pacote para meu tutorial",
    long_description="""
```
rafa(x, y)
```
para somar os numeros""",
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
