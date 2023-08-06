from distutils.core import setup
setup(
  name = 'locuspeerexplorer',         # How you named your package folder (MyLib)
  packages = ['locuspeerexplorer'],   # Chose the same as "name"
  version = '0.1.post7',      # Start with a small number and increase it with every change you make
  license='MIT',
  description = 'A package that lets you find similar community peers based off of functional or outcomee data',
  author = 'Locus Analytics',
  author_email = 'alee@locus.co',
  url = 'https://github.com/user/reponame',
  download_url =
  'https://github.com/LocusAnalytics/peer-explorer/archive/v0.1.post7.tar.gz',
  keywords = ['Economics', 'Peer Finder'],   # Keywords that define your package best
  install_requires=[
          'numpy',
          'pandas',
          'scipy',
          'fastdtw',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
