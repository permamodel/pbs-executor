"""Perform ingest operations in PBS."""

import os
import shutil
import yaml
from .file import IngestFile, Logger
from .verify import VerificationTool, VerificationError


file_exists = '''## File Exists\n
The file `{1}/{0}` already exists in the PBS data store.
The file has not been updated.
'''
file_moved = '''## File Moved\n
The file `{}` has been moved to `{}` in the PBS data store.
'''
file_not_verified = '''## File Verification Error\n
The file `{}` cannot be ingested into the PBS data store.
Error message:\n
    {}
'''


class ModelIngestTool(object):
    """
    Tool for uploading CMIP5-compatible model outputs into PBS.

    Parameters
    ----------
    ingest_file : str, optional
      Path to the configuration file (default is None).

    Attributes
    ----------
    ilamb_root : str
      Path to the ILAMB root directory.
    dest_dir : str
      Directory relative to ILAMB_ROOT where model outputs are stored.
    link_dir : str, optional
      Directory relative to ILAMB_ROOT where model outputs are linked.
    study_name : str, optional
      Name of modeling project or study; e.g., CMIP5.
    ingest_files : list
      List of files to ingest.
    make_public : bool
      Set to True to allow others to see and use ingested files.

    """
    def __init__(self, ingest_file=None):
        self.ilamb_root = ''
        self.dest_dir = ''
        self.link_dir = ''
        self.study_name = ''
        self.ingest_files = []
        self.make_public = True
        self.log = Logger(title='Model Ingest Tool Summary')
        if ingest_file is not None:
            self.load(ingest_file)

    def load(self, ingest_file):
        """
        Read and parse the contents of a configuration file.

        Parameters
        ----------
        ingest_file : str
          Path to the configuration file.

        """
        with open(ingest_file, 'r') as fp:
            cfg = yaml.safe_load(fp)
        self.ilamb_root = cfg['ilamb_root']
        self.dest_dir = cfg['dest_dir']
        self.link_dir = cfg['link_dir']
        self.study_name = cfg['study_name']
        for f in cfg['ingest_files']:
            self.ingest_files.append(IngestFile(f))
        self.make_public = cfg['make_public']

    def verify(self):
        """
        Check whether ingest files use the CMIP5 standard format.
        """
        for f in self.ingest_files:
            v = VerificationTool(f)
            try:
                v.verify()
            except VerificationError as e:
                msg = file_not_verified.format(f.name, e.msg)
                self.log.add(msg)
                if os.path.exists(f.name):
                    os.remove(f.name)
            else:
                f.data = v.model_name
                f.is_verified = True

    def move(self):
        """
        Move ingest files to the ILAMB MODELS directory.

        """
        models_dir = os.path.join(self.ilamb_root, self.dest_dir)
        for f in self.ingest_files:
            if f.is_verified:
                target_dir = os.path.join(models_dir, f.data)
                if not os.path.isdir(target_dir):
                    os.makedirs(target_dir)
                msg = file_moved.format(f.name, target_dir)
                try:
                    shutil.move(f.name, target_dir)
                except shutil.Error:
                    msg = file_exists.format(f.name, target_dir)
                    if os.path.exists(f.name):
                        os.remove(f.name)
                else:
                    if len(self.link_dir) > 0:
                        self.symlink(f)
                finally:
                    self.log.add(msg)

    def symlink(self, ingest_file):
        """
        Symlink a file into the PBS project directory.

        Parameters
        ----------
        ingest_file : IngestFile
          File for which symlink is crated.

        """
        src = os.path.join(self.ilamb_root,
                           self.dest_dir,
                           ingest_file.data,
                           ingest_file.name)
        dst_dir = os.path.join(self.ilamb_root,
                           self.link_dir,
                           self.study_name)
        if not os.path.isdir(dst_dir):
            os.makedirs(dst_dir)
        dst = os.path.join(dst_dir, ingest_file.name)
        os.symlink(src, dst)


class BenchmarkIngestTool(object):

    """Tool for uploading benchmark datasets into PBS."""

    def __init__(self):
        pass
