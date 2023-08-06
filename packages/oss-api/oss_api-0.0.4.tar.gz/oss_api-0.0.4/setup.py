from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="oss_api",
    version="0.0.4",
    author="kdd",
    author_email="kdd@imdc.be",
    description="api for IMDC's OSS server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/imdc/packages/oss_api",
    packages=find_packages(),
    install_requires=["requests"],
    scripts=["oss.py", "oss.bat"],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2.7",
    ],
)