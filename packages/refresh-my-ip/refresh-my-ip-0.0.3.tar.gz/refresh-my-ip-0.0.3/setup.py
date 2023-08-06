import setuptools
from setuptools import find_packages
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="refresh-my-ip",
    version="0.0.3",
    author="Troy Larson",
    author_email="troylar+github@pm.me",
    description="Refresh your ''my IP' in AWS security groups",
    url="https://github.com/troylar/refresh-my-ip",
    entry_points = {
        'console_scripts': ['refresh-my-ip=src.main:main'],
    },
    install_requires=[
        'boto==2.49.0',
        'boto3==1.9.202',
        'botocore==1.12.202',
        'Click==7.0',
        'docutils==0.14',
        'entrypoints==0.3',
        'flake8==3.7.8',
        'jmespath==0.9.4',
        'mccabe==0.6.1',
        'prettyprint==0.1.5',
        'pycodestyle==2.5.0',
        'pyflakes==2.1.1',
        'python-dateutil==2.8.0',
        's3transfer==0.2.1',
        'six==1.12.0',
        'urllib3==1.25.3',
    ],
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
