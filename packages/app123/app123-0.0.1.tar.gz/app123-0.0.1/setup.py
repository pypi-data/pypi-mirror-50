from setuptools import setup
import re

version = re.search('^__version__\s*=\s*"(.*)"', open("app/app.py").read(), re.M).group(1)

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="app123",
    version=version,
    description="example installable app",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["app"],
    entry_points={"console_scripts": ["app = app.app:main"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
