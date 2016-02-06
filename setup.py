import os

from setuptools import setup, find_packages


def readme():
    readme_file = os.path.join(os.path.dirname(__file__), 'README.md')
    with open(readme_file, 'r') as rf:
        return rf.read()

setup(
    name='snipping',
    author='Yi Tang',
    author_email='ssnailtang@gmail.com',
    version='0.1',
    description='Edit and run snippet in realtime',
    long_description=readme(),
    url='https://github.com/yittg/snipping',
    licence='MIT',
    packages=find_packages('.'),
    install_requires=[
        'prompt_toolkit',
        'pygments',
        'six',
    ],
    entry_points={
        'console_scripts': [
            'snipping = snipping.main:main',
        ],
    }
)
