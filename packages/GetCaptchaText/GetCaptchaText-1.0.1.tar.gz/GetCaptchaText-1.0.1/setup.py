from __future__ import print_function
from setuptools import setup, find_packages
import sys
 
setup(
    name='GetCaptchaText',
	version="1.0.1",
	author="guchen",
	author_email="281112162@qq.com",
	description="Gets the text content of the image captcha",
	long_description=open("README.rst").read(),
	license="MIT",
	url="",
	packages=['GetCaptchaText'],
	install_requires=["requests", "pytesseract", "pillow"],
	classifiers=[
	"Environment :: Web Environment",
	"Intended Audience :: Developers",
	"Operating System :: OS Independent",
	"Topic :: Text Processing :: Indexing",
	"Topic :: Utilities",
	"Topic :: Internet",
	"Topic :: Software Development :: Libraries :: Python Modules",
	"Programming Language :: Python",
	"Programming Language :: Python :: 2",
	"Programming Language :: Python :: 2.6",
	"Programming Language :: Python :: 2.7",
	],
	)
