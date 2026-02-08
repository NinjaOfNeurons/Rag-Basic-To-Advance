from setuptools import setup, find_packages
import os

# Read requirements
def read_requirements():
    with open('requirements.txt') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name='rag-cli',
    version='1.0.0',
    packages=find_packages(),  # This will find cli, cli.commands, src, etc.
    include_package_data=True,
    install_requires=read_requirements(),
    entry_points={
        'console_scripts': [
            'rag=cli.main:cli',
        ],
    },
    python_requires='>=3.8',
)