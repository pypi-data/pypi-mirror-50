=============
process_fastq
=============


.. image:: https://img.shields.io/pypi/v/process_fastq.svg
        :target: https://pypi.python.org/pypi/process_fastq

.. image:: https://img.shields.io/travis/mskcc/process_fastq.svg
        :target: https://travis-ci.org/mskcc/process_fastq

.. image:: https://readthedocs.org/projects/process-fastq/badge/?version=latest
        :target: https://process-fastq.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/mskcc/process_fastq/shield.svg
     :target: https://pyup.io/repos/mskcc/rhshah/process_fastq/
     :alt: Updates

.. image:: https://pyup.io/repos/github/mskcc/process_fastq/python-3-shield.svg
     :target: https://pyup.io/repos/mskcc/rhshah/process_fastq/
     :alt: Python 3


This package will help process, merge and link fastq in user specified directory from manifest file


* Free software: Apache Software License 2.0
* Documentation: https://process-fastq.readthedocs.io.

Usage
-----

Usage can be found here: https://process-fastq.readthedocs.io/en/latest/usage.html


Features
--------

1. Given Manifest file, path to location of raw fastq, path to where they need to linked:
  a. Get all the folders for the samples and the fastq file
  b. Check quickly the lenght of the reads if read length is not the same use the shorter read length and trim the fastq
  c. Merge the final fastq if comming from multiple runs. 
  d. Link all the fastq with the folder structure in user provided location

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
