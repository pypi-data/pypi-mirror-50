from setuptools import setup
setup(
  name = 'pyarc',
  packages = ['pyarc', "pyarc.data_structures", "pyarc.algorithms", "pyarc.qcba", "pyarc.utils"],
  version = '1.0.11',
  description = 'An implementation of CBA algorithm',
  author = 'Jiří Filip',
  author_email = 'j.f.ilip@seznam.cz',
  url = 'https://github.com/jirifilip/pyARC',
  download_url = 'https://github.com/jirifilip/pyARC/archive/1.0.tar.gz',
  keywords = ['classification', 'CBA', 'association rules', "machine learning"],
  classifiers = [],
  install_requires=['pandas']
)