"""Unit tests for the pbs_executor package."""

import os
import yaml


ingest_file = 'test_ingest.yaml'
model_file = 'test_model.txt'
benchmark_file = 'test_benchmark.txt'
log_file = 'index.html'
tmp_dir = 'tmp'
link_dir = 'link'
study_name = 'PBS'


def make_files(upload_file):
    cfg = dict()
    cfg['ilamb_root'] = os.getcwd()
    cfg['dest_dir'] = tmp_dir
    cfg['link_dir'] = link_dir
    cfg['study_name'] = study_name
    cfg['ingest_files'] = [upload_file]
    cfg['make_public'] = True
    cfg['overwrite_files'] = False
    with open(ingest_file, 'w') as fp:
        yaml.safe_dump(cfg, fp, default_flow_style=False)


def make_model_files():
    with open(model_file, 'w') as fp:
        fp.write('This is a test model output file.\n')
    make_files(model_file)


def make_benchmark_files():
    with open(benchmark_file, 'w') as fp:
        fp.write('This is a test benchmark data file.\n')
    make_files(benchmark_file)
