# coding: utf-8

from setuptools import setup


requires = ["requests>=2.14.2"]


setup(
    name='lineworks',
    version='0.0.1',
    description='It is a package that implements the server API and the Talk Bot API among the LINE WORKS APIs.',
    url='https://github.com/0yan/lineworks-api',
    author='Rei Suzuki',
    author_email='re1yanwork@gmail.com',
    license='MIT',
    keywords='LINE WORKS',
    packages=[
        'lineworks',
    ],
    install_requires=requires,
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ],
)