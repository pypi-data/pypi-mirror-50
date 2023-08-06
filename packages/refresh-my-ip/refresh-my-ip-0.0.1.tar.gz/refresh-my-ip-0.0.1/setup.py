import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
with open('requirements.txt') as f:
    requirements = (f.read)().splitlines()


setuptools.setup(
    name="refresh-my-ip",
    version="0.0.1",
    author="Troy Larson",
    author_email="troylar+github@pm.me",
    description="Refresh your \"my IP\" in AWS security groups",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/troylar/refresh-my-ip",
    entry_points = {
        'console_scripts': ['refresh-my-ip=src.main:main'],
    },
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
