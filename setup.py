# The python setup file

from setuptools import setup, find_packages

import versioneer

with open("requirements.txt") as reqs:
    requirements = reqs.read()

setup(
    name="esm_mongodb_check",
    author="Paul Gierz",
    author_email="pgierz@awi.de",
    python_requires=">=3.6, <3.10",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    description="The ESM Tools database checker",
    entry_points={
        "console_scripts": ["esm_database_check=esm_mongodb.cli:main"]
        },
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=requirements,
    license="GNU General Public License v2",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
)
