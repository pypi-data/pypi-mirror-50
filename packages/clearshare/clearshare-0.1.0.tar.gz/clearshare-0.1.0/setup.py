#!/usr/bin/env python
try:
    from setuptools import setup
    args = {}
except ImportError:
    from distutils.core import setup
    print("""\
*** WARNING: setuptools is not found.  Using distutils...
""")

from setuptools import setup
try:
    from pypandoc import convert_file
    read_md = lambda f: convert_file(f, 'rst')
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")
    read_md = lambda f: open(f, 'r').read()

setup(name='clearshare',
      version='0.1.0',
      description='Data management REST API for ClearSHARE.',
      author='ClearFoundation',
      author_email='developer@clearfoundation.com',
      url='https://gitlab.com/clearos/clearfoundation/clearshare',
      license='GPL-3.0',
      install_requires=[
          "datacustodian==0.3.1"
      ],
      packages=['clearshare'],
      scripts=['clearshare/clearshare_app.py'],
      package_data={'clearshare': ['../docker/*',
                                   '../docker/specs/*',
                                   '../docker/specs/global/*',
                                   '../docker/specs/ipfs/*',
                                   '../docker/deploy/*']},
      include_package_data=True,
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Natural Language :: English',
          'Operating System :: MacOS',
          'Operating System :: Unix',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.7'
      ],
     )
