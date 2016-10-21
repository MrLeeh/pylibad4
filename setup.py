#! /usr/bin/env python
# !-*- coding: utf-8 -*-
"""
:author: Stefan Lehmann
:email: stefan.st.lehmann@gmail.com
:created: 2016-10-11

"""
import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand
import versioneer


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


cmdclass = versioneer.get_cmdclass()
cmdclass.update({'test': PyTest})


setup(
    name='pylibad4',
    version=versioneer.get_version(),
    description='Python wrapper for BMCMs LIBAD4',
    author='Stefan Lehmann',
    author_email='stefan.st.lehmann@gmail.com',
    packages=['pylibad4'],
    install_requires=['future'],
    provides=['pylibad4'],
    url='https://github.com/MrLeeh/pylibad4',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2',
        'Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator'
    ],
    cmdclass=cmdclass
)