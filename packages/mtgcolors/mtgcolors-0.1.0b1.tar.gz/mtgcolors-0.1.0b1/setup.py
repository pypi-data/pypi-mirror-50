from setuptools import setup, find_packages
import os
import datetime


def formatIsoAsDigits():
    return datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")


version = "0.1.0b"
if os.environ.get("CI_COMMIT_TAG"):
    version = os.environ["CI_COMMIT_TAG"]
else:
    version += formatIsoAsDigits()

with open("README.md") as f:
    readme = f.read()

setup(
    name="mtgcolors",
    version=version,
    author="aloisdg",
    author_email="aloisdg@protonmail.com",
    description="MtgColors is module to detail mtg colors",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/aloisdegouvello/mtgcolors",
    packages=find_packages(exclude=("tests", "docs")),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
)
