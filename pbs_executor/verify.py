"""Verify that ingest files follow the CMIP5 standard format."""

import os
from netCDF4 import Dataset


class VerificationError(Exception):
    """
    Raise this exception when a file doesn't pass a verification test.

    Parameters
    ----------
    msg : str
      A human-readable message.

    Attributes
    ----------
    msg : str
      A human-readable message.

    """
    def __init__(self, msg):
        self.msg = ': '.join([type(self).__name__, msg])

    def __str__(self):
        return self.msg


class VerificationTool(object):
    """
    Tool for verifying that files are ILAMB-compatible.

    Parameters
    ----------
    file : str
      The name of a file to verify.

    Attributes
    ----------
    file : str
      The name of a file to verify.
    parts : list
      Parts of the filename (see Notes below).
    variable_name : str or None
      CMIP5 short variable name.

    """
    def __init__(self, file):
        self.file = file
        self.parts = []
        self.variable_name = None

    def is_netcdf(self):
        """
        Check whether a file is netCDF.

        """
        try:
            Dataset(self.file.name)
        except IOError as e:
            raise VerificationError(e.message)

    def parse_filename(self):
        """
        Break a filename into its component parts.

        """
        base, ext = os.path.splitext(self.file.name)
        self.parts = base.split('_')
        self.parts.append(ext)

    def verify(self):
        """
        Run all checks.

        A file that passes all checks is verified.

        """
        self.is_netcdf()
        self.parse_filename()


class ModelVerificationTool(VerificationTool):
    """
    Tool for verifying that model output files are CMIP5-compatible.

    Parameters
    ----------
    file : str
      The name of a file to verify.

    Attributes
    ----------
    file : str
      The name of a file to verify.
    parts : list
      Parts of the filename (see Notes below).
    variable_name : str or None
      CMIP5 short variable name.
    mip_table : str or None
      MIP table name.
    model_name : str or None
      Model name.
    experiment : str or None
      Experiment type.
    ensemble_member : str or None
      CMIP5 ensemble member.
    temporal_subset : str or None
      Time period covered by model

    Notes
    -----
    A CMIP5-compatible file name takes the following form:

        filename = <variable name>_<MIP table>_<model>_<experiment>_<ensemble_member>[_<temporal subset>].nc

    An example:

        tas_Amon_HADCM3_ historical_r1i1p1_185001-200512.nc

    """
    def __init__(self, file):
        super(ModelVerificationTool, self).__init__(file)
        self.mip_table = None
        self.model_name = None
        self.experiment = None
        self.ensemble_member = None
        self.temporal_subset = None

    def is_netcdf3_data_model(self):
        """
        Check whether a netCDF file uses the classic data model.

        """
        d = Dataset(self.file.name)
        if not d.data_model in ['NETCDF3_CLASSIC', 'NETCDF4_CLASSIC']:
            msg = 'NetCDF: File must use classic data model'
            raise VerificationError(msg)

    def filename_has_model_name(self):
        """
        Check that the filename includes a model name.

        """
        try:
            self.model_name = self.parts[2]
        except IndexError:
            msg = 'Model name not found'
            raise VerificationError(msg)

    def verify(self):
        """
        Run all checks.

        A file that passes all checks is verified.

        """
        super(ModelVerificationTool, self).verify()
        self.is_netcdf3_data_model()
        self.filename_has_model_name()


class BenchmarkVerificationTool(VerificationTool):
    """
    Tool for verifying that benchmark data files are ILAMB-compatible.

    Parameters
    ----------
    file : str
      The name of a file to verify.

    Attributes
    ----------
    file : str
      The name of a file to verify.
    parts : list
      Parts of the filename (see Notes below).
    variable_name : str or None
      CMIP5 short variable name.

    Notes
    -----
    ILAMB benchmark data file names can take two forms:

        filename = <variable name>.nc
        filename = <variable name>_<lon-resolution>_<lat-resolution>.nc

    The first is for point data, the second for gridded data.

    Examples:

        swe.nc
        tas_0.5x0.5.nc

    """
    def __init__(self, file):
        super(BenchmarkVerificationTool, self).__init__(file)
