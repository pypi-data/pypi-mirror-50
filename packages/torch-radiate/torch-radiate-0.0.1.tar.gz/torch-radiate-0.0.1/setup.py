import pathlib

from setuptools import find_packages, setup

# The text of the README file
README_CONTENT = (pathlib.Path(__file__).parent / "README.md").read_text()

setup(
    name='torch-radiate',
    version='0.0.1',
    description='Automatic deep learning research report generator',
    long_description=README_CONTENT,
    long_description_content_type='text/markdown',
    author='Benoit Anctil-Robitaille',
    author_email='benoit.anctil-robitaille.1@ens.etsmtl.ca',
    license='MIT',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7"],
    packages=find_packages(exclude=("tests",)),
    install_requires=[]
)
