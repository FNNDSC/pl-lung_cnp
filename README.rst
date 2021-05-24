pl-lung_cnp
===========

.. image:: https://img.shields.io/docker/v/fnndsc/pl-lung_cnp?sort=semver
    :target: https://hub.docker.com/r/fnndsc/pl-lung_cnp

.. image:: https://img.shields.io/github/license/fnndsc/pl-lung_cnp
    :target: https://github.com/FNNDSC/pl-lung_cnp/blob/master/LICENSE

.. image:: https://github.com/FNNDSC/pl-lung_cnp/workflows/ci/badge.svg
    :target: https://github.com/FNNDSC/pl-lung_cnp/actions


.. contents:: Table of Contents


Abstract
--------

This application houses a set of images that can be used in Normal/COVID/Pneumonia testing of COVIDNET


Description
-----------

``lung_cnp`` is a ChRIS-based application that simply copies a set of DICOM images to its output directory. The plugin is used as a convenient delivery vehicle containing images suitable for testing and further development.


Usage
-----

.. code::

        lung_cnp                                                        \
            [--dir <dir>]                                               \
            [-h] [--help]                                               \
            [--json]                                                    \
            [--man]                                                     \
            [--meta]                                                    \
            [--savejson <DIR>]                                          \
            [-v <level>] [--verbosity <level>]                          \
            [--version]                                                 \
            <outputDir>


Arguments
~~~~~~~~~

.. code::

        [--dir <dir>]
        An optional override directory to copy to the <outputDir>.
        Note, if run from a containerized version, this will copy
        a directory from the *container* file system.

        [-h] [--help]
        If specified, show help message and exit.

        [--json]
        If specified, show json representation of app and exit.

        [--man]
        If specified, print (this) man page and exit.

        [--meta]
        If specified, print plugin meta data and exit.

        [--savejson <DIR>]
        If specified, save json representation file to DIR and exit.

        [-v <level>] [--verbosity <level>]
        Verbosity level for app. Not used currently.

        [--version]
        If specified, print version number and exit.


Getting inline help is:

.. code:: bash

    docker run --rm fnndsc/pl-lung_cnp lung_cnp --man

Run
~~~

You need to specify input and output directories using the `-v` flag to `docker run`.


.. code:: bash

    docker run --rm -u $(id -u)                             \
         -v $(pwd)/out:/outgoing                            \
        fnndsc/pl-lung_cnp lung_cnp                         \
        /outgoing


Development
-----------

Build the Docker container:

.. code:: bash

    docker build -t local/pl-lung_cnp .

Run unit tests:

.. code:: bash

    docker run --rm local/pl-lung_cnp nosetests

Examples
--------

Copy the embedded lung CT data to the ``out`` directory
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

    # Here, files are copied as localuser
    mkdir out && chmod 777 out
    docker run --rm -u $(id -u)                                 \
        -v  $(pwd)/out:/outgoing                                \
        fnndsc/pl-lung_cnp lung_cnp                             \
        /outgoing

Copy a user specified directory to the ``out`` directory
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

    # Here, files are copied as root
    mkdir out && chmod 777 out
    docker run --rm                                             \
        -v  $(pwd)/out:/outgoing                                \
        fnndsc/pl-lung_cnp lung_cnp                             \
        --dir /etc                                              \
        /outgoing

.. image:: https://raw.githubusercontent.com/FNNDSC/cookiecutter-chrisapp/master/doc/assets/badge/light.png
    :target: https://chrisstore.co
