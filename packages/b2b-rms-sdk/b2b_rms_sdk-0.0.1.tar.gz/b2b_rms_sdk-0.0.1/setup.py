import setuptools
from setuptools import setup

setup(
    name="b2b_rms_sdk",
    version="0.0.1",
    description="Helper SDK for b2b_rms apis",
    url="https://github.com/shuttl-tech/b2b_rms_sdk",
    author="Jayesh Hathila",
    author_email="jayesh.hathila@shuttl.com",
    license="MIT",
    packages=setuptools.find_packages(),
    classifiers=["Programming Language :: Python :: 3.7"],
    install_requires=["pyshuttlis", "requests"],
    extras_require={"test": ["pytest", "pytest-runner", "pytest-cov", "pytest-pep8"]},
)
