from setuptools import setup, find_packages
setup(
  name = 'vibra',
  packages = find_packages(),
  version = 'v1.7.1',#####
  license='MIT',
  description = 'A non-finished add-on to Tensorflow',
  author = 'PerceptronV',
  author_email = 'perceptronv@gmail.com',
  url = 'https://github.com/PerceptronV/vibra', #######
  download_url = 'https://github.com/PerceptronV/vibra/archive/v1.7.1.tar.gz', ######
  keywords = ['Tensorflow', 'add-on'],
  install_requires=[
      'numpy',
  ],
  classifiers=[  # Optional
    # How mature is this project? Common values are
    #   3 - Alpha
    #   4 - Beta
    #   5 - Production/Stable
    'Development Status :: 3 - Alpha',

    # Pick your license as you wish
    'License :: OSI Approved :: MIT License',

    # Specify the Python versions you support here. In particular, ensure
    # that you indicate whether you support Python 2, Python 3 or both.
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
      'Programming Language :: Python :: 3.7',
  ],
)
