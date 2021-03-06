"""The `ingest` module contains classes for uploading files into the
PBS.

"""
import os
import shutil
import yaml
from .file import IngestFile, Logger
from .verify import (ModelVerificationTool, BenchmarkVerificationTool,
                     VerificationError)
from .utils import makedirs


file_exists = '''## File Exists\n
The file `{1}/{0}` already exists in the PBS data store.
The file has not been updated.
'''
file_protected = '''## File Protected\n
The file `{}` is protected in the PBS data store.
The base files provided by ILAMB may only be modified by an administrator.
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


class IngestTool(object):
    """
    Toolbase for ingesting files into the PBS.

    Parameters
    ----------
    ingest_file : str, optional
      Path to the configuration file (default is None).

    Attributes
    ----------
    ilamb_root : str
      Path to the ILAMB root directory.
    dest_dir : str
      Directory relative to ILAMB_ROOT where ingested files are stored.
    link_dir : str, optional
      Directory relative to ILAMB_ROOT where ingested files are linked.
    project_name : str, optional
      Name of modeling project or study; e.g., CMIP5, MsTMIP, PBS.
    source_name : str
      A name under which uploaded files can be grouped. Required for 
      grouping uploaded benchmark datasets.
    ingest_files : list
      List of files to ingest.
    make_public : bool
      Set to True to allow others to see and use ingested files.
    overwrite_files : bool
      Set to True to allow users to overwrite uploaded files. Only an
      administrator can overwrite files distributed with ILAMB.

    """
    def __init__(self, ingest_file=None):
        self.ilamb_root = ''
        self.dest_dir = ''
        self.link_dir = ''
        self.project_name = ''
        self.source_name = ''
        self.ingest_files = []
        self.make_public = True
        self.overwrite_files = False

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
        self.project_name = cfg['project_name']
        self.source_name = cfg['source_name']
        for f in cfg['ingest_files']:
            self.ingest_files.append(IngestFile(f))
        self.make_public = cfg['make_public']
        self.overwrite_files = cfg['overwrite_files']


    def symlink(self, src_dir, ingest_file, append_source_name=False):
        """
        Symlink a file into the PBS project directory.

        Parameters
        ----------
        src_dir : str
          The directory path that contains the source file to link.
        ingest_file : IngestFile
          File for which symlink is crated.
        append_source_name : bool, optional
          Set to True to append group name to path (default is False).

        """
        src = os.path.join(src_dir, ingest_file.name)
        dst_dir = os.path.join(self.ilamb_root, self.link_dir,
                               self.project_name)
        if not os.path.isdir(dst_dir):
            makedirs(dst_dir, mode=0775)
        dst_filename = ingest_file.name
        if append_source_name:
            dst_filename += '.' + self.source_name
        dst = os.path.join(dst_dir, dst_filename)
        if os.path.islink(dst):
            os.remove(dst)
        os.symlink(src, dst)


class ModelIngestTool(IngestTool):

    """Tool for adding CMIP5-compatible model outputs to the PBS."""

    def __init__(self, ingest_file=None):
        super(ModelIngestTool, self).__init__(ingest_file=None)
        self.log = Logger(title='Model Ingest Tool Summary')
        if ingest_file is not None:
            self.load(ingest_file)

    def verify(self):
        """
        Check whether ingest files use the CMIP5 standard format.

        """
        for f in self.ingest_files:
            v = ModelVerificationTool(f)
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

        Notes
        -----
        The directory structures for an uploaded model output
        should look like:

        .. code-block:: bash

           MODELS
            |
            +-- SiBCASA
                 |
                 +-- test_model_output.txt

           MODELS-by-project
            |
            +-- PBS
                 |
                 +-- test_model_output.txt -> MODELS/SibCASA/test_model_output.txt

        """
        models_dir = os.path.join(self.ilamb_root, self.dest_dir)
        for f in self.ingest_files:
            if f.is_verified:
                target = target_dir = os.path.join(models_dir, f.data)
                if not os.path.isdir(target_dir):
                    makedirs(target_dir, mode=0775)
                if self.overwrite_files:
                    target = os.path.join(target_dir, f.name)
                msg = file_moved.format(f.name, target)
                try:
                    shutil.move(f.name, target)
                except IOError:
                    msg = file_protected.format(target)
                    if os.path.exists(f.name):
                        os.remove(f.name)
                except shutil.Error:
                    msg = file_exists.format(f.name, target)
                    if os.path.exists(f.name):
                        os.remove(f.name)
                else:
                    if len(self.link_dir) > 0:
                        self.symlink(target_dir, f)
                finally:
                    self.log.add(msg)


class BenchmarkIngestTool(IngestTool):

    """Tool for adding benchmark datasets to the PBS."""

    def __init__(self, ingest_file=None):
        super(BenchmarkIngestTool, self).__init__(ingest_file=None)
        self.log = Logger(title='Benchmark Ingest Tool Summary')
        if ingest_file is not None:
            self.load(ingest_file)

    def verify(self):
        """
        Check whether ingest files use an ILAMB-compatible format.

        """
        for f in self.ingest_files:
            v = BenchmarkVerificationTool(f)
            try:
                v.verify()
            except VerificationError as e:
                msg = file_not_verified.format(f.name, e.msg)
                self.log.add(msg)
                if os.path.exists(f.name):
                    os.remove(f.name)
            else:
                f.data = v.variable_name
                f.is_verified = True

    def move(self):
        """Move ingest files to the ILAMB DATA directory.

        Notes
        -----
        The directory structures for an uploaded benchmark dataset
        should look like:

        .. code-block:: bash

           DATA
            |
            +-- lai
                 |
                 +-- CSDMS
                      |
                      +-- test_benchmark.txt

           DATA-by-project
            |
            +-- PBS
                 |
                 +-- test_benchmark.txt.CSDMS -> DATA/lai/CSDMS/test_benchmark.txt

        """
        data_dir = os.path.join(self.ilamb_root, self.dest_dir)
        for f in self.ingest_files:
            if f.is_verified:
                target = target_dir = os.path.join(data_dir, f.data,
                                                   self.source_name)
                if not os.path.isdir(target_dir):
                    makedirs(target_dir, mode=0775)
                if self.overwrite_files:
                    target = os.path.join(target_dir, f.name)
                msg = file_moved.format(f.name, target)
                try:
                    shutil.move(f.name, target)
                except IOError:
                    msg = file_protected.format(target)
                    if os.path.exists(f.name):
                        os.remove(f.name)
                except shutil.Error:
                    msg = file_exists.format(f.name, target)
                    if os.path.exists(f.name):
                        os.remove(f.name)
                else:
                    if len(self.link_dir) > 0:
                        self.symlink(target_dir, f, append_source_name=True)
                finally:
                    self.log.add(msg)
