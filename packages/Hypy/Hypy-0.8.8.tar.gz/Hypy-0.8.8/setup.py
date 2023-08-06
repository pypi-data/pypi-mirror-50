#
from inspect import cleandoc

from setuptools import setup, Extension


__version__ = '0.8.8'


ext = Extension("_estraiernative",
                ["estraiernative.c"],
                libraries=["estraier"],
                include_dirs=["/usr/include/estraier", "/usr/include/qdbm"],
                )

setup(
    name="Hypy",
    description='Pythonic wrapper for Hyper Estraier',
    author='Yusuke YOSHIDA',
    author_email='usk@nrgate.jp',
    maintainer='Cory Dodt',
    maintainer_email='pypi@spam.goonmill.org',
    url='http://goonmill.org/hypy/',
    download_url='http://hypy-source.goonmill.org/archive/tip.tar.gz',
    version=__version__,
    ext_modules=[ext],
    zip_safe=False,
    packages=['hypy'],

    classifiers=[
      'Development Status :: 4 - Beta',
      'Environment :: Console',
      'Environment :: Web Environment',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
      'Operating System :: POSIX',
      'Programming Language :: Python',
      'Topic :: Software Development :: Libraries',
      'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
      ],
    extras_require={
        'dev': [
            'pytest>=3.0.2',
            'pytest-cov>=2.5.1',
            'pytest-flakes>=2.0.0',
            'tox',
        ],
    },
)
