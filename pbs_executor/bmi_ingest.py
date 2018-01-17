"""Define the BMI for the PBS ingest tools."""

from basic_modeling_interface import Bmi
from .ingest import ModelIngestTool, BenchmarkIngestTool


class BmiIngestToolBase(Bmi):

    _component_name = 'IngestToolBase'

    def __init__(self):
        self._config_file = None
        self._tool = None
        self._time = self.get_start_time()

    def get_component_name(self):
        return self._component_name

    def initialize(self, filename):
        self._config_file = filename
        self._tool.load(self._config_file)

    def update(self):
        if self.get_current_time() < self.get_end_time():
            self._time = self.get_end_time()
            self._tool.verify()
            self._tool.move()

    def update_until(self, time):
        self.update()

    def finalize(self):
        self._tool = None

    def get_input_var_names(self):
        return ()

    def get_output_var_names(self):
        return ()

    def get_start_time(self):
        return 0.0

    def get_end_time(self):
        return 1.0

    def get_current_time(self):
        return self._time

    def get_time_step(self):
        return 1.0

    def get_time_units(self):
        return 's'


class BmiModelIngestTool(BmiIngestToolBase):

    _component_name = 'ModelIngestTool'

    def __init__(self):
        super(BmiModelIngestTool, self).__init__()
        self._tool = ModelIngestTool()


class BmiBenchmarkIngestTool(BmiIngestToolBase):

    _component_name = 'BenchmarkIngestTool'

    def __init__(self):
        super(BmiBenchmarkIngestTool, self).__init__()
        self._tool = BenchmarkIngestTool()
