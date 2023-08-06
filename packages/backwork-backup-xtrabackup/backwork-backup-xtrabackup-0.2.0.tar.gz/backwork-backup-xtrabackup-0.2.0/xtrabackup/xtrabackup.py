"""Xtrabackup for Backwork
"""

import subprocess
import logging

LOG = logging.getLogger(__name__)


class XtraBackupBackup(object):
    """Xtrabackup plugin for Backwork"""
    command = "xtrabackup"

    def __init__(self, args, extra):
        self.args = args
        self.extra = extra
        self.result = ""

    @classmethod
    def parse_args(cls, subparsers):
        """Add argument parser for the plugin."""
        subparsers.add_parser(cls.command, description=cls.__doc__)

    def backup(self):
        """Perform the backup."""
        LOG.info("starting XtraBackup backup...")

        cmd = ["xtrabackup", "--backup"] + self.extra

        try:
            self.result = subprocess.check_output(
                cmd, stderr=subprocess.STDOUT)
            LOG.info("output:\n\n\t%s", "\n\t".join(self.result.split("\n")))
            LOG.info("backup complete")

        except subprocess.CalledProcessError as error:
            self.result = error.output
            LOG.error("failed to back up XtraBackup database")
            LOG.error("return code was %s", error.returncode)
            LOG.error("output:\n\n\t%s", "\n\t".join(self.result.split("\n")))
            LOG.error("backup process failed")
            raise error
