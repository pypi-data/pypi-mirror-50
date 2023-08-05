#!/usr/bin/env python3

import emojipedia_search as project

from setuptools import setup, find_packages
import os

def here(*path):
    return os.path.join(os.path.dirname(__file__), *path)

def get_file_contents(filename):
    with open(here(filename), 'r', encoding='utf8') as fp:
        return fp.read()

setup(
    name = project.__name__,
    description = project.__doc__.strip(),
    long_description=get_file_contents('README.md'),
    long_description_content_type='text/markdown',
    url = 'https://gitlab.com/nul.one/' + project.__name__,
    download_url = 'https://gitlab.com/nul.one/{1}/-/archive/{0}/{1}-{0}.tar.gz'.format(project.__version__, project.__name__),
    version = project.__version__,
    author = project.__author__,
    author_email = project.__author_email__,
    license = project.__license__,
    packages = [ project.__name__ ],
    entry_points={ 
        'console_scripts': [
            'emojipedia={0}.__main__:cli'.format(project.__name__),
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Utilities',
    ],
    install_requires = [
        'beautifulsoup4>=4.4.1,<5.0',
        'requests>=2.18.4,<3.0',
        'clipboard==0.0.4',
    ],
    python_requires=">=3.4.6",
)

