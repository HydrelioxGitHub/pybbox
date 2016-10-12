from distutils.core import setup
setup(
  name = 'pybbox',
  packages = ['pybbox'], # this must be the same as the name above
  install_requires = ['netaddr','requests'],
  version = '0.0.5-alpha',
  description = 'a simple python3 library for the Bouygues BBox Routeur API',
  author = 'Hydreliox',
  author_email = 'hydreliox@gmail.com',
  url = 'https://github.com/HydrelioxGitHub/pybbox', # use the URL to the github repo
  download_url = 'https://github.com/HydrelioxGitHub/pybbox/tarball/0.0.5-alpha',
  keywords = ['bbox', 'Bouygues', 'routeur', 'API'], # arbitrary keywords
  classifiers = [],
)