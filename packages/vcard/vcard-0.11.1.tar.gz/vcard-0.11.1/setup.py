#!/usr/bin/env python
"""Setup configuration"""

from setuptools import setup

from vcard import __author__, __doc__, __email__, __license__, __maintainer__, __package__, __url__, __version__

setup(
    name=__package__,
    version=__version__,
    description="vCard validator, class and utility functions",
    long_description=__doc__,
    url=__url__,
    keywords="vCard vCards RFC 2426 RFC2426 validator",
    packages=[__package__],
    setup_requires=["isodate"],
    install_requires=["isodate", "six"],
    entry_points={"console_scripts": ["%(package)s=%(package)s.%(package)s:main" % {"package": __package__}]},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Topic :: Text Processing",
        "Topic :: Utilities",
    ],
    test_suite="tests",
    author=__author__,
    author_email=__email__,
    maintainer=__maintainer__,
    maintainer_email=__email__,
    download_url="http://pypi.python.org/pypi/vcard/",
    platforms=["POSIX", "Windows"],
    license=__license__,
    obsoletes=["vcard_module"],
)
