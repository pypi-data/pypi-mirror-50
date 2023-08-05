#!/usr/bin/env python3

from setuptools import find_packages, setup
from setuptools.command.develop import develop
from setuptools.command.install import install
import subprocess


def symlink():
    package = 'franklab_msdrift'
    symlink_cmd = (f'ml-link-python-module {package} '
                   f'`ml-config package_directory`/{package}')
    subprocess.run(symlink_cmd, shell=True)


class PostDevelopCommand(develop):
    """Post-installation for development mode."""

    def run(self):
        symlink()
        develop.run(self)


class PostInstallCommand(install):
    """Post-installation for installation mode."""

    def run(self):
        symlink()
        install.run(self)


INSTALL_REQUIRES = ['numpy', 'scikit-learn', 'scipy']
TESTS_REQUIRE = []

setup(
    name='franklab_msdrift',
    version='0.1.3.dev0',
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
