from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="sentinel1_bdc_beta",
    version="0.0.1",
    author="Diego Silva",
    description="Sentinel image processing library 1.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # packages=[""],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[],
    dependency_links=['https://github.com/diisilva/sentinel1_bdc_beta']
)
