from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fhandle:
    long_description = fhandle.read()

setup(
    name="secstructartist",
    version="1.0.10",
    author="David Bickel",
    description="Module to visualize protein secondary structure in matplotlib plots",
    license="OSI Approved :: GNU General Public License v3 (GPLv3)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/bio2byte/constava/",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Visualization",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "Development Status :: 5 - Production/Stable"
    ],
    python_requires=">=3.6, <3.11",
    install_requires=[
        "numpy",
        "matplotlib",
    ],
)
