#Setup file for Pandora program

from setuptools import setup

setup(name='APT_stats',
      version='0.0.3',
      description='Python Tool for APT Mass Statistics',
      url='https://victorgarric.github.io/APT_stats/',
      license='GNU GPLv3',
      author='Victor Garric',
      author_email='victor.garric@gmail.com',
      keywords='TEM image analysis precipitate cluster clustering',
      install_requires=['mendeleev','tableprint','matplotlib','numpy'],
      packages=['APT_stats'],
      zip_safe=False)