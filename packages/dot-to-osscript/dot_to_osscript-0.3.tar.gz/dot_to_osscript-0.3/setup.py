from setuptools import setup
from info import info

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name=info.get("name"),
      version=info.get("version"),
      description=info.get("description"),
      long_description=long_description,
      long_description_content_type='text/markdown',
      url=info.get("url"),
      author=info.get("author"),
      author_email=info.get("author_email"),
      license=info.get("license"),
      packages=[info.get("name")],
      install_requires=info.get("install_requires"),
      python_requires=">=3",
      zip_safe=False)
