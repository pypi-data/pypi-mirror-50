from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()



setup(
    name="epiVIA",
    version="1.1.0",
    author="Wenliang Wang",
    author_email="wangwl.me@gmail.com",
    description="Virial Integration Analysis with epigenetic data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wangwl/epiVIA",
    install_requires=['pysam', 'pandas', 'biopython', 'requests', 'pybedtools'],
    entry_points={'console_scripts': ['epiVIA = src.chimera:main']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)