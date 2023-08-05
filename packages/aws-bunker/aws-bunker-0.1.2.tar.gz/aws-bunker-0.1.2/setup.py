import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aws-bunker",
    version="0.1.2",
    author="Andy Klier, Gus Clemens",
    author_email="andyklier@gmail.com",
    description="bunker is a command line program for creating a dev/backup ec2 in AWS. It will install software, and clone your git repos, then it will transfer ignored files from your machine to the ec2.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/shindagger/bunker",
    packages=['bunker'],
    include_package_data=True,
    install_requires= ['setuptools', 'boto3'],
    entry_points = {
        'console_scripts': ['bunker=bunker.bunker:bunker'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
