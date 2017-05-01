
from setuptools import setup, find_packages
import sys, os

setup(name='jpipes',
    version='0.9.5',
    description="Jenkins Pipeline Automation",
    long_description="Jenkins Pipeline Automation",
    classifiers=[], 
    keywords='',
    author='BJ Dierkes',
    author_email='derks@datafolklabs.com',
    url='https://github.com/derks/jpipes',
    license='BSD-three-clause',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    test_suite='nose.collector',
    install_requires=[
        ### Required to build documentation
        # "Sphinx >= 1.0",
        ### Required for testing
        # "nose",
        # "coverage",
        ### Required to function
        'cement',
        'requests',
        'pyYaml',
        'colorlog',
        ],
    setup_requires=[],
    entry_points="""
        [console_scripts]
        jpipes = jpipes.cli.main:main
    """,
    namespace_packages=[],
    )
