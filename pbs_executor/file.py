"""Perform file operations in PBS."""

import markdown


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
