from distutils.core import setup

setup(
    # Application name:
    name="micro-kit",

    # Version number (initial):
    version="0.7.0",

    # Application author details:
    author="Chanpreet Singh Chhabra",
    author_email="chanpreet.chhabra@innovaccer.com",

    # Packages
    packages=["microkit"],

    # Include additional files into the package
    include_package_data=True,

    # Details
    url="https://pypi.org/project/micro-kit/",

    #
    # license="LICENSE.txt",
    description="A helper kit to power the APIs",

    # long_description=open("README.txt").read(),

    # Dependent packages (distributions)
    install_requires=[
        "flask",
    ],
)