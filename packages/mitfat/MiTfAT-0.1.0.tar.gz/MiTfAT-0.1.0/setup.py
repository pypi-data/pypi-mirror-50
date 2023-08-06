import io
import os
import re

from setuptools import find_packages
from setuptools import setup


def read(filename):
    filename = os.path.join(os.path.dirname(__file__), filename)
    text_type = type(u"")
    with io.open(filename, mode="r", encoding='utf-8') as fd:
        return re.sub(text_type(r':[a-z]+:`~?(.*?)`'), text_type(r'``\1``'), fd.read())


setup(
    name="MiTfAT",
    version="0.1.0",
    url="https://gitlab.tuebingen.mpg.de/vbokharaie/mitfat/",
    license='MIT',

    author="Vahid Samadi Bokharaie",
    author_email="vahid.bokharaie@tuebingen.mpg.de",

    description="A python-based fMRI Analysis Tool. ",
    long_description=read("README.rst"),

    packages=find_packages(exclude=('tests', 'venv')),

    test_suite='nose.collector',
    tests_require=['nose'],
    package_data={'mitfat': ['datasets/*.*', 'sample_info_file.txt',]},
    include_package_data=True,

    install_requires=[
    'seaborn==0.9.0',
    'pandas==0.25.0',
    'numpy==1.16.4',
    'scipy==1.3.0',
    'matplotlib==3.1.1',
    'nibabel==2.5.0',
    'nilearn==0.5.2',
    'scikit_learn==0.21.3',
    'openpyxl',
    ],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
