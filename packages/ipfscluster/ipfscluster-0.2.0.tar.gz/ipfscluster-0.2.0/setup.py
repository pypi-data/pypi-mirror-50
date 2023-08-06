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

setup(name='ipfscluster',
      version='0.2.0',
      description='HTTP Client for IPFS Cluster.',
      long_description=read_md('README.md'),
      author='ClearFoundation',
      author_email='developer@clearfoundation.com',
      url='https://gitlab.com/clearos/clearfoundation/py-ipfs-cluster-api',
      license='GPL-3.0',
      install_requires=[
          "argparse",
          "pyparsing",
          "termcolor",
          "pyyaml",
          "requests",
          "ipfshttpclient"
      ],
      packages=['ipfscluster'],
      scripts=[],
      package_data={'ipfscluster': ['templates/*']},
      include_package_data=True,
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Intended Audience :: Other Audience',
          'Natural Language :: English',
          'Operating System :: MacOS',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.7'
      ],
     )
