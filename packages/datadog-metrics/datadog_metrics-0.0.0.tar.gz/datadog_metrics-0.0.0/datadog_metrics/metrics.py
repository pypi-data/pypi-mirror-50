"""
For usage instructions, follow the official Datadog API reference
https://docs.datadoghq.com/api/?lang=python#metrics
"""
import json
import sys

from awsglue.utils import getResolvedOptions
from datadog import api, initialize

from peloconfig import ConfigManager


APP_NAME = "glue_jobs"
REGION_NAME = "us-east-1"
SECRET_NAME = "datadog"


class DatadogClient(object):
    def __init__(self, config=None):
        self._args = getResolvedOptions(sys.argv, ['JOB_NAME', 'env'])

        if not config:
            config_manager = ConfigManager(
                environment=self._args['env'],
                appname=APP_NAME,
                region_name=REGION_NAME
            )
            config = json.loads(config_manager.get_value(SECRET_NAME))

        initialize(**config)

        self._default_tags = [
            'env:{}'.format(self._args['env']),
            'job_name:{}'.format(self._args['JOB_NAME'])
        ]

    def send_metric(self, **kwargs):
        if 'tags' in kwargs:
            kwargs['tags'] += self._default_tags
        else:
            kwargs['tags'] = self._default_tags

        api.Metric.send(**kwargs)

