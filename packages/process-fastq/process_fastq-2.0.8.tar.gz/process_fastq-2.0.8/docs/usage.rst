=====
Usage
=====

To use process_fastq in a project::

    import process_fastq
    process_fastq.run(sample_id, request_id, run_id, fastq_path, output_path, cutadapt_path)

To use process_fastq from cli::

    Usage: process_fastq [OPTIONS]

        Options:
        -s, --sample-id TEXT            Sample id to get the fastq files can be
                                        either IGO sample id or Investigator sample
                                        id (eg: -s EDD_ret_pt049_cf02)  [required]
        -p, --request-id TEXT           IGO request id to get the fastq files.
                                        (eg:-p Project_05500_GB or -p 05500_GB)
        -r, --run-id TEXT               Run id to get the fastq files, can be
                                        specified multiple times (eg:-r PITT_0376 -r
                                        PITT_0378)
        -fp, --fastq-path PATH          Full path to fastq files  [required]
        -op, --output-path PATH         Full path to where we link the output files
                                        [required]
        -cp, --cutadapt-path PATH       Full path to location of cutadapt executable
                                        [required]
        -l, --expected-read-length INTEGER
                                        Expected read length from the fastq file
        --version                       Show the version and exit.
        -v, --verbosity LVL             Either CRITICAL, ERROR, WARNING, INFO or
                                        DEBUG
        --help                          Show this message and exit.

Example commandline:

    .. code-block:: console
    
       $ process_fastq \
       -p request_id \
       -s smaple_name \
       -r RunID \
       -fp /path/to/fastq/directory \
       -op /path/to/output/directory \
       -cp /path/to/cutadapt
    
    .. code

To use link_fastq_juno.py from cli::

Usage: link_fastq_juno.py [OPTIONS]

Options:
  -m, --manifest-file PATH        Manifest file having information about run
                                  id and sample id to get the fastq files (eg:
                                  -m Project_05500_GB_manifest.xslx)
                                  [required]
  -p, --request-id TEXT           IGO request id to get the fastq files.
                                  (eg:-p Project_05500_GB or -p 05500_GB)
                                  [required]
  -fp, --fastq-path PATH          Full path to fastq files  [required]
  -op, --output-path PATH         Full path to where we link the output files
                                  [required]
  -cp, --cutadapt-path PATH       Full path to location of cutadapt executable
                                  [required]
  -pfp, --process-fastq-path PATH
                                  Full path to location of cutadapt executable
                                  [required]
  -l, --expected-read-length INTEGER
                                  Expected read length from the fastq file
  --version                       Show the version and exit.
  -v, --verbosity LVL             Either CRITICAL, ERROR, WARNING, INFO or
                                  DEBUG
  --help                          Show this message and exit.

Example commandline:

    .. code-block:: console
    
       $ python3 link_fastq_juno.py \
       -p request_id \
       -m /path/to/manifest.xlsx \
       -pfp /path/to/process_fastq \
       -fp /path/to/fastq/directory \
       -op /path/to/output/directory \
       -cp /path/to/cutadapt
    
    .. code