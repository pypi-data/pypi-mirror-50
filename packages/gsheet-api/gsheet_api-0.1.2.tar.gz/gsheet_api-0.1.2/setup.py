import os
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="gsheet_api",
    version="0.1.2",
    author="Branden Colen",
    author_email="brandencolen@gmail.com",
    description=("Easily and efficiently manage a Google Sheet"),
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    keywords="google sheet api pandas dataframe",
    packages=['gsheet_api'],
    url="https://github.com/brandenc40/gsheet-api",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta"
    ]
)
