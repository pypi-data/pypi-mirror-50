"""Handling packaging and distribution of this package."""
from __future__ import absolute_import
from setuptools import setup


setup(
    name='rotest-xml',
    version="0.1.0",
    description="Xml output handler for rotest",
    long_description=open("README.rst").read(),
    license="MIT",
    keywords="rotest testing system django unittest",
    install_requires=[
        'rotest',
        'future',
        'xmltodict',
    ],
    extras_require={
        "dev": [
            "flake8",
            "pylint",
        ]
    },
    python_requires=">=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*",
    entry_points={
        "rotest.result_handlers": [
            "xml = "
            "rotest_xml:XmlHandler",
        ],
    },
    packages=['rotest_xml'],
    zip_safe=False,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Testing',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Operating System :: MacOS',
    ],
)
