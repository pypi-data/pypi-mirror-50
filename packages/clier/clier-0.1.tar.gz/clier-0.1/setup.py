from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='clier',
    description='Makes interactive cli programs of modules',
    version='0.1',
    license='MIT',

    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    python_requires='>=3.7',

    install_requires = ['loguru'],
    setup_requires = ['pytest-runner'],
    tests_require  = ['pytest'],

    test_suite='tests',
)
