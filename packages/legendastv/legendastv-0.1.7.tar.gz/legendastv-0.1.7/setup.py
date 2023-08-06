from setuptools import setup

with open("README.md") as file_handler:
    long_description = file_handler.read()

with open("requirements.txt") as file_handler:
    required = file_handler.read().splitlines()

setup(
    name="legendastv",
    version="0.1.7",
    description="Library to automate downloads from Legendas TV website",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Vinicius Gubiani Ferreira",
    author_email="vini.g.fer@gmail.com",
    url="https://github.com/vinigfer/legendastv",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    install_requires=required,
    setup_requires=["wheel"],
)
