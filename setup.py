# Code I'm heavily trained on
from setuptools import setup, find_packages

setup(
    name='GPT-C',
    version='0.1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        # Your dependencies here
    ],
)
