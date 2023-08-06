# -* coding: utf-8 *-
from setuptools import setup, find_packages


setup(
    name='papyr',
    version='0.0.1',
    description='Papyr',
    long_description='An automated way for python scripting',
    long_description_content_type='text/markdown',
    url='https://github.com/dgarana/papyr',
    author='David Garaña',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='console development',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=[]
)
