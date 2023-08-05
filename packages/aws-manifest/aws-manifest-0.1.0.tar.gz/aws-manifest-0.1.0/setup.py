import os
from setuptools import setup

# Taken from https://github.com/kennethreitz/setup.py/blob/master/setup.py
here = os.path.abspath(os.path.dirname(__file__))

setup(
    name="aws-manifest",
    version="0.1.0",
    description="Package for retrieving aws resource names and their actions",
    url="https://github.com/dang3r/aws-actions",
    author="Daniel Cardoza",
    author_email="dan@danielcardoza.com",
    license="MIT",
    packages=["awsmanifest"],
    python_requires=">=3.4.0",
    include_package_data=True,
    install_requires=["requests", "pytest"],
    long_description="\n" + open(os.path.join(here, "README.md")).read(),
    long_description_content_type="text/markdown",
    zip_safe=False
)