"""Unit tests for the pbs_executor package."""

import os
import re
import yaml


ingest_file = 'test_ingest.yaml'
model_file = 'test_model.txt'
benchmark_file = 'test_benchmark.txt'
log_file = 'index.html'
models_dir = 'MODELS'
data_dir = 'DATA'
models_link_dir = 'MODELS-link'
data_link_dir = 'DATA-link'
project_name = 'PBS'
source_name = 'CSDMS'


def make_files(upload_file, dest_dir, link_dir):
    cfg = dict()
    cfg['ilamb_root'] = os.getcwd()
    cfg['dest_dir'] = dest_dir
    cfg['link_dir'] = link_dir
    cfg['project_name'] = project_name
    cfg['source_name'] = source_name
    cfg['ingest_files'] = [upload_file]
    cfg['make_public'] = True
    cfg['overwrite_files'] = False
    with open(ingest_file, 'w') as fp:
        yaml.safe_dump(cfg, fp, default_flow_style=False)


def make_model_files():
    with open(model_file, 'w') as fp:
        fp.write('This is a test model output file.\n')
    make_files(model_file, models_dir, models_link_dir)


def make_benchmark_files():
    with open(benchmark_file, 'w') as fp:
        fp.write('This is a test benchmark data file.\n')
    make_files(benchmark_file, data_dir, data_link_dir)


def find_in_file(filename, search_str):
    with open(filename, 'r') as fp:
        for line in fp:
            if re.search(search_str, line):
                return True
    return False
