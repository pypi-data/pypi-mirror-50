========
date-cli
========

.. image:: https://travis-ci.org/Jhengsh/date-cli.svg?branch=master
   :target: https://travis-ci.org/Jhengsh/date-cli
   :alt: Build Status

.. image:: https://img.shields.io/pypi/v/date-cli.svg
   :target: https://pypi.org/project/date-cli/
   :alt: Latest Release

This package provides date command line.

* date_range: help you generate date between 2 date(format: yyyymmdd)
* month_range: help you generate date between 2 month(format: yyyymm)

------------
Installation
------------

Method 1: Using PyPI

    $ pip install date-cli

Method 2: Using git

    $ pip install git+https://github.com/Jhengsh/date-cli.git

--------
Tuturial
--------

Basic Use::

    $ date_range -s 20200225 -e 20200305 | awk '{print "python execute.py --yyyymmdd "$1";"}'
    # python execute.py --yyyymmdd 20200225;
    # python execute.py --yyyymmdd 20200226;
    # python execute.py --yyyymmdd 20200227;
    # python execute.py --yyyymmdd 20200228;
    # python execute.py --yyyymmdd 20200229;
    # python execute.py --yyyymmdd 20200301;
    # python execute.py --yyyymmdd 20200302;
    # python execute.py --yyyymmdd 20200303;
    # python execute.py --yyyymmdd 20200304;
    # python execute.py --yyyymmdd 20200305;

    $ month_range -s 202001 -e 202003                                                                          jhengsh@Jhengshs-MBP
    # 202001
    # 202002
    # 202003