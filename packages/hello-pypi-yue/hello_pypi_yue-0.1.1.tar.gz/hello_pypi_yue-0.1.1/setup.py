"""The setup script for installing the package."""
from setuptools import setup, find_packages, Extension
from distutils.core import setup, Extension

# read the contents of the README
with open('Readme.md') as README_md:
    README = README_md.read()

setup(
    name='hello_pypi_yue',
    version='0.1.1',
    description='The Pypi test',
    keywords=' '.join([
        'Pypi',
    ]),
    classifiers=[
        'License :: Free For Educational Use',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    url='https://lossyou.com',
    author='OuYanghaoyue',
    author_email='tonyue@gmail.com',
    long_description=README,
    long_description_content_type="text/markdown",
    license='Proprietary',
    packages=find_packages(exclude=['tests', '*.tests', '*.tests.*']),
    package_data={'hello_pypi': ['ROMs/*.nes']},
    install_requires=[''],
    entry_points={
        'console_scripts': [
            'say_hello=say_hello:say',
        ]
    }
)
