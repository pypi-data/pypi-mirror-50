from setuptools import setup

with open("README.txt", "r") as fh:
    long_description = fh.read()

setup(
    name='CeleryStalk',
    version='1.0.1',
    author='Rudy Venguswamy',
    author_email='rvenguswamy@vmware.com',
    packages=['CeleryStalk'],
    scripts=[],
    url='http://pypi.python.org/pypi/CeleryStalk/',
    license='LICENSE.txt',
    description='Change Large CSVs Faster with Easy Parallel Processing',
    long_description=long_description,
    install_requires=[
        "celery >= 4.2.0",
        "redis >= 2.10.5",
    ],
)