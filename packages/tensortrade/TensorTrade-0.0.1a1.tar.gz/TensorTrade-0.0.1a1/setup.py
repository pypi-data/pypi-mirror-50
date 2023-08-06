from setuptools import setup
from setuptools import find_packages

long_description = """
A reinforcement learning library for training, evaluating, and deploying robust trading agents with TF2.
"""

setup(name='TensorTrade',
      version='0.0.1a1',
      description='A reinforcement learning library for training, evaluating, and deploying robust trading agents with TF2.',
      long_description=long_description,
      author='Adam King',
      author_email='adamjking3@gmail.com',
      url='https://github.com/notadamking/tensortrade',
      download_url='https://github.com/notadamking/tensortrade/tarball/0.0.1',
      license='GPLv3',
      install_requires=[
          'numpy',
          'pandas',
          'sklearn',
          'gym',
          'gin-config',
      ],
      extras_require={
          'exchanges': ['ccxt', 'stochastic'],
          'tuning': ['hyperopt'],
          'tests': [],
      },
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Intended Audience :: Developers',
          'Intended Audience :: Education',
          'Intended Audience :: Science/Research',
          'Intended Audience :: Financial and Insurance Industry',
          'Intended Audience :: Information Technology',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Office/Business :: Financial :: Investment',
          'Topic :: Scientific/Engineering :: Artificial Intelligence',
      ],
      packages=find_packages())
