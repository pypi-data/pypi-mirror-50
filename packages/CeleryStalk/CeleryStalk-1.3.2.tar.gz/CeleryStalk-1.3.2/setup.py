from setuptools import setup



setup(
    name='CeleryStalk',
    version='1.3.2',
    author='Rudy Venguswamy',
    author_email='rvenguswamy@vmware.com',
    packages=['CeleryStalk'],
    scripts=[],
    url='http://pypi.python.org/pypi/CeleryStalk/',
    license='LICENSE.txt',
    description='Change Large CSVs Faster with Easy Parallel Processing',
    long_description="README.txt",
    install_requires=[
        "celery >= 4.2.0",
        "redis >= 2.10.5",
    ],
)