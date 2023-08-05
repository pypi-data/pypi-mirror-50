import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bolapy",
    version="0.0.1",
    author="Rafael Rayes",
    author_email="rafa@rayes.com",
    description="Um pacote de tutorial",
    long_description="""
use bola assim:
```
bolapy.bola()
```
para imprimir algo""",
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
