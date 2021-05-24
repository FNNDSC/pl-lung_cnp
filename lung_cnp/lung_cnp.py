#
# lung_cnp fs ChRIS plugin app
#
# (c) 2021 Fetal-Neonatal Neuroimaging & Developmental Science Center
#                   Boston Children's Hospital
#
#              http://childrenshospital.org/FNNDSC/
#                        dev@babyMRI.org
#

from    chrisapp.base           import ChrisApp

from    os                      import listdir
from    os.path                 import isfile, join
from    distutils.dir_util      import copy_tree
import  sys



Gstr_title = """

 _
| |
| |_   _ _ __   __ _     ___ _ __  _ __
| | | | | '_ \./ _` |   / __| '_ \| '_ \.
| | |_| | | | | (_| |  | (__| | | | |_) |
|_|\__,_|_| |_|\__, |   \___|_| |_| .__/
                __/ |_____        | |
               |___/______|       |_|


"""

Gstr_synopsis = """
    NAME

       lung_cnp

    SYNOPSIS

        lung_cnp                                                        \\
            [--dir <dir>]                                               \\
            [-h] [--help]                                               \\
            [--json]                                                    \\
            [--man]                                                     \\
            [--meta]                                                    \\
            [--savejson <DIR>]                                          \\
            [-v <level>] [--verbosity <level>]                          \\
            [--version]                                                 \\
            <outputDir>

    BRIEF EXAMPLE

        * Bare bones execution

            mkdir out
            docker run --rm -u $(id -u)                                 \\
                -v  $(pwd)/out:/outgoing                                \\
                fnndsc/pl-lung_cnp lungcnp                              \\
                /outgoing

    DESCRIPTION

        `lung_cnp` simply copies internal lungCT DICOM data dir to the
        <outputDir>. If an optional [--dir <dir>] is passed, then contents
        of <dir> are copied instead.

        This is a successor to ``pl-lungct`` with additional, more meaningful
        DICOM images. In all other respects it is identical to ``pl-lungct``.

    ARGS

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

    EXAMPLES

    Copy the embedded lung CT data to the ``out`` directory
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # Here, files are copied as localuser
    mkdir out && chmod 777 out
    docker run --rm -u $(id -u)                                 \\
        -v  $(pwd)/out:/outgoing                                \\
        fnndsc/pl-lung_cnp lung_cnp                             \\
        /outgoing

    Copy a user specified directory to the ``out`` directory
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # Here, files are copied as root
    mkdir out && chmod 777 out
    docker run --rm                                             \\
        -v  $(pwd)/out:/outgoing                                \\
        fnndsc/pl-lung_cnp lung_cnp                             \\
        --dir /etc                                              \\
        /outgoing

"""


class Lung_cnp(ChrisApp):
    """
    This application houses a set of images that can be used in Normal/COVID/Pneumonia testing of COVIDNET
    """
    PACKAGE                 = __package__
    TITLE                   = 'A ChRIS FS plugin that carries lung images of Normal/COVID/Pneumonia exemplars'
    CATEGORY                = 'Data'
    TYPE                    = 'fs'
    ICON                    = ''   # url of an icon image
    MIN_NUMBER_OF_WORKERS   = 1    # Override with the minimum number of workers as int
    MAX_NUMBER_OF_WORKERS   = 1    # Override with the maximum number of workers as int
    MIN_CPU_LIMIT           = 1000 # Override with millicore value as int (1000 millicores == 1 CPU core)
    MIN_MEMORY_LIMIT        = 200  # Override with memory MegaByte (MB) limit as int
    MIN_GPU_LIMIT           = 0    # Override with the minimum number of GPUs as int
    MAX_GPU_LIMIT           = 0    # Override with the maximum number of GPUs as int

    # Use this dictionary structure to provide key-value output descriptive information
    # that may be useful for the next downstream plugin. For example:
    #
    # {
    #   "finalOutputFile":  "final/file.out",
    #   "viewer":           "genericTextViewer",
    # }
    #
    # The above dictionary is saved when plugin is called with a ``--saveoutputmeta``
    # flag. Note also that all file paths are relative to the system specified
    # output directory.
    OUTPUT_META_DICT = {}

    def define_parameters(self):
        """
        Define the CLI arguments accepted by this plugin app.
        Use self.add_argument to specify a new app argument.
        """
        self.add_argument('--dir',
                          dest          ='dir',
                          type          = str,
                          default       = '/usr/local/src/data/images',
                          optional      = True,
                          help          = 'directory override')

    def run(self, options):
        """
        Define the code to be run by this plugin app.
        """
        print(Gstr_title)
        print('Version: %s' % self.get_version())

        for k,v in vars(options).items():
            print("%20s: %-40s" % (k, v))
        print("")

        if len(options.dir):
            print("Copying tree %s to %s..." % (options.dir, options.outputdir))
            l_file : list = [f for f in listdir(options.dir) if isfile(join(options.dir, f))]
            copy_tree(options.dir, options.outputdir)
            print("Copied...")
            for f in l_file:
                print(f)
            sys.exit(0)
        else:
            print("No directory specified and no copy performed.")
            sys.exit(1)

    def show_man_page(self):
        """
        Print the app's man page.
        """
        print(Gstr_synopsis)
