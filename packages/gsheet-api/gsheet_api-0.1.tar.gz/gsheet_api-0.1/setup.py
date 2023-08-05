import os
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name="gsheet_api",
      version="0.1",
      author="Branden Colen",
      author_email="brandencolen@gmail.com",
      description=("Easily and efficiently manage a Google Sheet"),
      long_description=read('README.md'),
      long_description_content_type='text/markdown',
      keywords="google sheet api pandas dataframe easy",
      packages=['gsheet_api'],
      url="https://github.com/brandenc40/gsheet-api")