from distutils.core import setup
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='vro_package_diff',
    version='2.0.0',
    author="Ludovic Rivallain",
    author_email='ludovic.rivallain+vropackagediff@gmail.com',
    packages=setuptools.find_packages(),
    description=
    "Provide a table-formated diff of two VMware vRealize Orchestrator packages.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "terminaltables",  # Pretty print a table
        "colored",  # A bit of colors from fancy term
        "click",  # CLI arguments management
    ],
    classifiers=[
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Environment :: Console"
    ],
    entry_points={
        'console_scripts': [
            'vro-diff=vro_package_diff.__main__:main',
        ],
    })
