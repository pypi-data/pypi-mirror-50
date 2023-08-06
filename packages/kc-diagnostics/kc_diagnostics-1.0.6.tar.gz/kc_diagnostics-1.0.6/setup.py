import setuptools
from codecs import open
from os import path
from kc_diagnostics import __version__

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
  long_description = f.read()

setuptools.setup(
  name="kc_diagnostics",
  version=__version__,
  author="Fawad Mazhar",
  author_email="fawad.mazhar@nordcloud.com",
  description="Package to generate diagnostics messages.",
  long_description=long_description,
  long_description_content_type="text/markdown",
  keywords=['AWS', 'IoT', 'Diagnostics', 'Lambda'],
  url="https://github.com/fawad1985/kc-diagnostics",
  download_url="https://github.com/fawad1985/kc-diagnostics/archive/{}.tar.gz".format(__version__),
  packages=['kc_diagnostics'],
  include_package_data=True,
  install_requires=[
      'boto3',
      'pathlib'
  ],
  classifiers=[
      "Programming Language :: Python :: 2.7",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
  ]
)