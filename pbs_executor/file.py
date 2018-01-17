"""Perform file operations in PBS."""

import os
import yaml
import markdown
from netCDF4 import Dataset
from ConfigParser import SafeConfigParser
from . import data_directory


header = '''<!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>PBS Ingest Tool Summary</title>
</head>
<body>
'''
footer = '''
</body>
</html>
'''


def get_region_labels_txt(regions_file):
    """Get the labels for custom ILAMB regions from a text file.

    Parameters
    ----------
    regions_file : str
        A text file containing ILAMB custom region definitions.

    Returns
    ----------
    list
        A list of custom region labels.

    """
    labels = []
    with open(regions_file, 'r') as fp:
        lines = fp.readlines()
    for line in lines:
        labels.append(line.split(',')[0])
    return labels


def get_region_labels_ncdf(regions_file):
    """Get the labels for custom ILAMB regions from a netCDF file.

    Parameters
    ----------
    regions_file : str
        A netCDF file containing ILAMB custom region definitions.

    Returns
    ----------
    list
        A list of custom region labels.

    """
    labels = region_labels = []
    fid = Dataset(regions_file)
    for k, v in fid.variables.iteritems():
        if len(v.dimensions) == 2 and "labels" in v.ncattrs():
            labels = fid.variables[v.labels][...]
    for label in labels:
        region_labels.append(label.lower().encode('utf-8'))
    return region_labels


class IlambConfigFile(object):

    """Tool for generating an ILAMB config file."""

    sources_file = os.path.join(data_directory, 'cmip5-variables.yaml')

    def __init__(self,
                 variables,
                 relationships=False,
                 config_file='ilamb.cfg',
                 title='Permafrost Benchmark System'):

        """Set parameters for an ILAMB config file.

        Parameters
        ----------
        variables : array_like, required
            A string, list, or tuple of model output variables, using
            CMIP5 short names (e.g., *gpp*, not *Gross Primary
            Production*).
        relationships : boolean, optional
            Set to calculate relationships between the input variables
            (default is False).
        config_file : str, optional
            The name of the ILAMB config file (default is
            **ilamb.cfg**).
        title : str, optional
            A name for the ILAMB run (default is *Permafrost Benchmark
            System*).

        Examples
        --------
        Set up and write an ILAMB config file for *gpp*:

        >>> f = IlambConfigFile('gpp')
        >>> f.setup()
        >>> f.write()

        """
        if type(variables) is str:
            self.variables = variables,
        else:
            self.variables = variables
        self.sources = None
        self.config_file = config_file
        self.config = dict()
        self.has_relationships = relationships
        if len(self.variables) < 2 and self.has_relationships:
            raise TypeError('Two variables are needed for a relationship')
        self.title = title

    def setup(self):
        """Generate settings for an ILAMB config file."""
        for var in self.variables:
            self.read(var)

        if self.has_relationships and len(self.variables) > 1:
            self.get_sources()
            self.add_relationships()

    def get_template_file(self, var_name):
        """Get path to a variable's template file.

        Parameters
        ----------
        var_name : str
            The CMIP5 short name for a variable.

        """
        base_file = var_name + '.cfg.tmpl'
        tmpl_file = os.path.join(data_directory, base_file)
        if not os.path.isfile(tmpl_file):
            raise IOError('Not a file: ' + base_file)
        else:
            return tmpl_file

    def read(self, var_name):
        """Read configuration information from a template file.

        Parameters
        ----------
        var_name : str
            The CMIP5 short name for a variable.

        """
        tmpl_file = self.get_template_file(var_name)
        self.config[var_name] = SafeConfigParser()
        self.config[var_name].read(tmpl_file)

    def get_sources(self):
        """Load long name and benchmark source info for all variables."""
        with open(self.sources_file, 'r') as fp:
            self.sources = yaml.safe_load(fp)

    def add_relationships(self):
        """Add all relationships for a variable."""
        for var in self.variables:
            all_vars = list(self.variables)
            all_vars.pop(all_vars.index(var))
            relations = self._make_relationships(all_vars)
            if len(all_vars) > 1:
                rel_string = ','.join(relations)
            else:
                rel_string = relations[0]
            self.config[var].set(self.sources[var]['benchmark_source'],
                                 'relationships', rel_string)

    def write(self):
        """Write an ILAMB config file."""
        with open(self.config_file, 'w') as fp:
            self._write_header(fp)
            for var in self.variables:
                self.config[var].write(fp)

    def _write_header(self, ofp):
        header = '''
# Benchmark CMIP5-compatible model outputs against available datasets.

[h1: {}]
bgcolor = "#FFECE6"{}
'''.strip().format(self.title, '\n\n')
        ofp.write(header)

    def _make_relationships(self, var_list):
        relations = list()
        for var in var_list:
            src = '/'.join([self.sources[var]['long_name'],
                            self.sources[var]['benchmark_source']])
            relations.append('"' + src + '"')
        return relations


class IngestFile(object):
    """
    A file of model outputs or benchmark data to be ingested into PBS.

    Parameters
    ----------
    filename : str or None, optional
      The name of the file (default is None).

    Attributes
    ----------
    name : str
      The name of the file.
    is_verified : bool
      Set to True if the file is a verified model output or benchmark
      data file.
    data : str
      The name of the model (for a model output file) or of the
      variable in the file (for a benchmark dataset).

    """
    def __init__(self, filename=None):
        self.name = filename
        self.is_verified = False
        self.data = None


class Logger(object):
    """
    A tool to generate an HTML log file from Markdown messages.

    Parameters
    ----------
    title : str, optional
      The title of the log file.

    Attributes
    ----------
    data : str
      The contents of the log.

    """
    def __init__(self, title='Summary'):
        self.data = markdown.markdown('# {}'.format(title))
        self.write()

    def add(self, message):
        """
        Add a message to the log.

        Parameters
        ----------
        message : str
          A message.

        """
        self.data += markdown.markdown(message)
        self.write()

    def write(self):
        """
        Write the log file `index.html`.

        """
        with open('index.html', 'w') as fp:
            fp.write(header)
            fp.write(self.data)
            fp.write(footer)
