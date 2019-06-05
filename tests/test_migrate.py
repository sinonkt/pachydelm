import pytest
from pachydelm.migrate import migrate
# from pachydelm.core import PachydermAdminContext

@pytest.mark.usefixtures("ctx")
def test_answer(ctx):
    # print(ctx)
    print(ctx.migrations)
    assert 5 == 5

import click
import json
import ast
# from jsondiff import diff
from deepdiff import DeepDiff
import python_pachyderm
from pprint import pprint
import python_pachyderm.client.pps.pps_pb2 as proto
from pachydelm.utils import convert, map_nested_dicts_modify, force_number

from pachydelm.core import PachydermMigration

from google.protobuf.json_format import MessageToDict

# fields = [field.name for field in proto.PipelineInfo.DESCRIPTOR.fields]
# deprecated: scale_down_threshold
# no usecases/docs: hashtree_spec

fields = [
    "transform", "parallelism_spec", "egress", "update",
    "output_branch", "resource_requests",
    "resource_limits", "input", "description", "cache_size", "enable_stats",
    "reprocess", "batch", "max_queue_size", "service", "chunk_spec",
    "datum_timeout", "job_timeout", "salt", "standby", "datum_tries",
    "scheduling_spec", "pod_spec", "pod_patch"
]

ignored_from_diff_fields = [ 'created_at', 'salt', 'spec_commit', 'state']

@click.command()
@click.pass_obj
def test(ctx):
    """ test module"""
    click.echo('test something')
    migration = PachydermMigration(ctx)

    inspected = ctx.pps.inspect_pipeline('huhu')
    invalidKey = MessageToDict(inspected, including_default_value_fields=False)
    pipelineInfo = { convert(k) : v for k, v in invalidKey.items() if convert(k) not in ignored_from_diff_fields }
    map_nested_dicts_modify(pipelineInfo, force_number)
    with open('./configs/2019_06_04_221735_huhu_pipeline_oh_my_god.json', 'r') as f:
        loaded = json.loads(f.read())

    print("********************************* Inspect PipelineInfo *********************************")
    print(pipelineInfo)
    print("****************************************************************************************")
    print("************************************ load ConfigJson ***********************************")
    print(loaded)
    print("****************************************************************************************")
    print("*************************************** Diff *******************************************")
    ddiff = DeepDiff(pipelineInfo, loaded, verbose_level=2)
    pprint(ddiff, indent=2)
    print("****************************************************************************************")
    # print(
    # print(verify_is_pipeline_exists(ctx, 'test-pipeline'))
    # jobs = list(ctx.pps.list_job('test-pipeline').job_info)
    # list(map(lambda x: x, jobs))
    # pipelines = list(ctx.pps.list_pipeline().pipeline_info)
    # print(jobs)
    # print(pipelines)
    
    # print(jobs[0].state)
    # for job in jobs:
    #     print(job)
    # print(list(map(jobs.job_info, lambda x: x.state)))
    # print((jobs, lambda x: x.state)))
    # for job in enumerate(jobs):
    #     print(job)

    # filePath = '%s/eiei.json' % (ctx.pachydermConfigsDir)
    # migration.create_pipeline_from_file(filePath)