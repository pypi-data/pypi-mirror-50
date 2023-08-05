#!/usr/bin/env python3

from setuptools import find_packages, setup
from setuptools.command.develop import develop
from setuptools.command.install import install
import subprocess

symlink_cmd = 'ml-link-python-module franklab_msdrift $(ml-config package_directory)/franklab_msdrift'.split()


class PostDevelopCommand(develop):
    """Post-installation for development mode."""

    def run(self):
        subprocess.run(symlink_cmd, shell=True)
        develop.run(self)


class PostInstallCommand(install):
    """Post-installation for installation mode."""

    def run(self):
        subprocess.run(symlink_cmd, shell=True)
        install.run(self)


INSTALL_REQUIRES = ['numpy', 'scikit-learn', 'scipy']
TESTS_REQUIRE = []

setup(
    name='franklab_msdrift',
    version='0.1.2.dev0',
    license='',
    description=(''),
    author='',
    author_email='',
    url='',
    packages=find_packages(),
    install_requires=INSTALL_REQUIRES,
    tests_require=TESTS_REQUIRE,
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
    },
)
