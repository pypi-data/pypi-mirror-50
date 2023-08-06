# -*- coding: utf-8 -*-
"""File backup module for Monsoon
"""

import logging
import subprocess

LOGGER = logging.getLogger(__name__)


class FilesBackup(object):
    """Back up one or more files.

    It uses `tar -cz` and gzips the output. You can use any of the
    arguments supported by `tar`. Add a list of files and
    directories you want backed up as the last thing in the line.
    Use `tar --help` for more information.
    """
    command = "files"

    def __init__(self, args, extra):
        """Initialize a backup command given the arguments passed to CLI"""

        self.args = args
        self.extra = extra
        self.result = ""

    @classmethod
    def parse_args(cls, subparsers):
        """Create the `files` subparser for the `backup` command.
        :param subparsers: Main argument parser
        """
        fs_parser = subparsers.add_parser(cls.command, description=cls.__doc__)

        fs_parser.add_argument("-o", "--output", required=True,
                               help="output gzipped file path")

    def backup(self):
        """Backup one or more files."""
        LOGGER.info("starting file backup...")

        tar_cmd = ["tar", "-cz", "-f", self.args.output] + self.extra

        try:
            self.result = subprocess.check_output(tar_cmd, stderr=subprocess.STDOUT)
            LOGGER.info("output:\n\n\t%s", "\n\t".join(self.result.split("\n")))
            LOGGER.info("file backup complete")
        except Exception as error:
            LOGGER.error("Failed to backup files")
            raise error
