from setuptools import setup
setup(
  name = 'runpredictor',
  packages = ['RunPredictor'], 
  version = '1.0',
  description = 'A library predicting first innings score in odi,t-20 and ipl',
  author = 'Shivam Mitra',
  author_email = 'shivamm389@gmail.com',
  license = 'GPLv2',
  url = 'https://github.com/codophobia/RunPredictor', 
  download_url = 'https://github.com/codophobia/RunPredictor/tarball/1.0', 
  keywords = ['cricket', 'prediction'], 
  install_requires=[
          'numpy',
          'sklearn',
      ],
  classifiers = [],
)
