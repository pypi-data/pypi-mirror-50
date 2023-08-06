from distutils.core import setup
setup(
  name = 'vibra',
  packages = ['vibra'],
  version = 'v1.0',
  license='MIT',
  description = 'An add-on to Tensorflow',
  author = 'VERSUS',
  author_email = 'vursustechnology@gmail.com',
  url = 'https://github.com/PerceptronV/vibra', #######
  download_url = 'https://github.com/PerceptronV/vibra/archive/v1.0.tar.gz', ######
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

    # Indicate who your project is intended for
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',

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
