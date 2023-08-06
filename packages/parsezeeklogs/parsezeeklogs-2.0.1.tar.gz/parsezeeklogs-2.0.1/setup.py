import setuptools

setuptools.setup(
  name = 'parsezeeklogs',
  packages=['parsezeeklogs'],
  version = '2.0.1',
  description = 'A lightweight utility for programmatically reading and manipulating Zeek IDS (Bro IDS) log files and outputting into JSON or CSV format.',
  long_description = 'A lightweight utility for programmatically reading and manipulating Zeek IDS (Bro IDS) log files and outputting into JSON or CSV format.',
  author = 'Dan Gunter',
  author_email = 'dangunter@gmail.com',
  url = 'https://github.com/dgunter/parsezeeklogs',
  download_url = 'https://github.com/dgunter/parsezeeklogs/archive/v1.1.3.tar.gz',
  keywords = ['InfoSec', 'Bro IDS', 'security'],
  classifiers = [
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
)
