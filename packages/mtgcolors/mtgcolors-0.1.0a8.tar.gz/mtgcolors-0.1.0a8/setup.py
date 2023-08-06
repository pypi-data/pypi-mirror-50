from setuptools import setup, find_packages
import os

version = "0.1.0a8"
if os.environ.get("CI_COMMIT_TAG"):
    version = os.environ["CI_COMMIT_TAG"]
elif os.environ.get("CI_JOB_ID"):
    version = os.environ["CI_JOB_ID"]

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
