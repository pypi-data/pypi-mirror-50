#!/usr/bin/env python3

from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='breadpi',
	  version='1.0',
	  author='SB Components',
	  author_email='rd@sb-components.co.uk',
	  maintainer='SB Components',
	  maintainer_email='suppport@sb-components.co.uk',
	  url='https://github.com/sbcshop/BreadPi',
	  description='BreadPi hardware support package',
	  long_description=long_description,
	  download_url='https://github.com/sbcshop/BreadPi',
	  license='GNU',
	  py_modules=['breadpi'],
	  classifiers=[
			'License :: OSI Approved :: GNU Lesser General Public License v3 ('
			'LGPLv3)',
			'Intended Audience :: Developers',
			'Programming Language :: Python :: 3',
			]
	  )