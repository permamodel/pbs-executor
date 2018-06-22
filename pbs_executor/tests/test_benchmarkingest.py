"""Tests for the BenchmarkIngestTool class."""

from nose.tools import assert_true
from pbs_executor.ingest import BenchmarkIngestTool


def test_init():
    x = BenchmarkIngestTool()
    assert_true(isinstance(x, BenchmarkIngestTool))
