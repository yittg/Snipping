from setuptools import setup, find_packages


def readme():
    with open("README.rst", 'r') as rf:
        return rf.read()

setup(
    name='snipping',
    author='Yi Tang',
    author_email='ssnailtang@gmail.com',
    version='0.2',
    description='Edit and run snippet in real time',
    long_description=readme(),
    url='https://github.com/yittg/snipping',
    license='MIT',
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
    })
