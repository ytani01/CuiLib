import os
import sys
from setuptools import setup, find_packages

def read_requirements():
    """ Parse requirements from requirements.txt """
    reqs_path = os.path.join('.', 'requirements.txt')
    with open(reqs_path, 'r') as f:
        requirements = [line.rstrip() for line in f]
    return requirements

with open("README.md") as f:
    long_description =f.read()

setup(
    name='cuilib',
    version='0.0.4',
    description='Simple CUI(Command Line Interface) library',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Yoichi Tanibayashi',
    author_email='yoichi@tanibayashi.jp',
    url='https://github.com/ytani01/CuiLib/',
    license='MIT',
    classifiers=[
        "Development Status :: 3 - Alpha",
    ],
    install_requires=read_requirements(),
    packages=find_packages(exclude=('tests', 'docs')),
    python_requires='>=3.7',
)
