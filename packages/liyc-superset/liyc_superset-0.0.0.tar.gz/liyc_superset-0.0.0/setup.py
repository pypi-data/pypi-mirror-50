import io
import json
import os
import subprocess
import sys

from setuptools import find_packages, setup

if sys.version_info < (3, 6):
    sys.exit("Sorry, Python < 3.6 is not supported")

setup(
    name="liyc_superset",
    description=("A modern, enterprise-ready business intelligence web application"),
    long_description="",
    long_description_content_type="text/markdown",
    version="",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    scripts=["superset/bin/superset"],
    install_requires=[
        "bleach>=3.0.2, <4.0.0",
        "celery>=4.3.0, <5.0.0",
        "click>=6.0, <7.0.0",  # `click`>=7 forces "-" instead of "_"
        "colorama",
        "contextlib2",
        "croniter>=0.3.28",
        "cryptography>=2.4.2",
        "flask>=1.0.0, <2.0.0",
        "flask-appbuilder>=2.1.6, <2.3.0",
        "flask-caching",
        "flask-compress",
        "flask-talisman",
        "flask-migrate",
        "flask-wtf",
        "geopy",
        "gunicorn",  # deprecated
        "humanize",
        "idna",
        "isodate",
        "markdown>=3.0",
        "pandas>=0.24.2, <0.25.0",
        "parsedatetime",
        "pathlib2",
        "polyline",
        "pydruid>=0.5.2",
        "python-dateutil",
        "python-dotenv",
        "python-geohash",
        "pyyaml>=5.1",
        "requests>=2.22.0",
        "retry>=0.9.2",
        "selenium>=3.141.0",
        "simplejson>=3.15.0",
        "sqlalchemy>=1.3.5,<2.0",
        "sqlalchemy-utils>=0.33.2",
        "sqlparse",
        "wtforms-json",
    ],
    extras_require={
        "bigquery": ["pybigquery>=0.4.10", "pandas_gbq>=0.10.0"],
        "cors": ["flask-cors>=2.0.0"],
        "gsheets": ["gsheetsdb>=0.1.9"],
        "hive": ["pyhive[hive]>=0.6.1", "tableschema", "thrift>=0.11.0, <1.0.0"],
        "mysql": ["mysqlclient==1.4.2.post1"],
        "postgres": ["psycopg2-binary==2.7.5"],
        "presto": ["pyhive[presto]>=0.4.0"],
    },
    author="",
    author_email="",
    url="",
    classifiers=["Programming Language :: Python :: 3.7"],
)
