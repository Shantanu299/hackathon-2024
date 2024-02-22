import importlib
import logging
import os
import sys
import traceback
from typing import Optional, Any

import yaml
import concurrent.futures
from dataclasses import dataclass, field

from app.workflow.jobs.base_job import BaseJob

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


@dataclass
class Engine:
    workflow_name: str
    seed: Optional[Any] = field(default=None)
    workflow_config: dict = field(init=False)
    context: dict = field(init=False)

    def __post_init__(self):
        workflow_path = os.path.join(
            ROOT_DIR, "config.yml"
        )
        with open(workflow_path, encoding='UTF-8') as data:
            self.workflow_config = yaml.load(data, Loader=yaml.FullLoader)
        self.context = {}

    def arrange_jobs(self):
        workflow = self.workflow_config['workflows'][self.workflow_name]
        if not self.workflow_config.get('jobs'):
            return workflow['jobs']

        job_sequences = []
        for job_name in workflow['jobs']:
            if job_name not in self.workflow_config['jobs']:
                job_sequences.append(job_name)
            else:
                job_config = self.workflow_config['jobs'][job_name]
                if job_config.get('parallel'):
                    if isinstance(job_sequences[-1], list):
                        job_sequences[-1].append(job_name)
                    else:
                        job_sequences.append([job_name])
                else:
                    job_sequences.append(job_name)
        logger.info("Job sequence: %s", job_sequences)
        return job_sequences

    @staticmethod
    def convert_job_to_class(job_name):
        return ''.join(map(lambda string: string.capitalize(), job_name.split('_')))

    def load_job(self, job_name):
        module = importlib.import_module(
            f".{job_name}", package="app.workflow.jobs"
        )
        return getattr(module, self.convert_job_to_class(job_name))

    def get_context(self, job_name):
        job_config = self.workflow_config['jobs'].get(job_name)
        if job_config is None:
            return {}
        job_contexts = job_config.get('context', [])
        return {job_name: self.context[job_name] for job_name in job_contexts}

    def execute_job(self, job_name):
        # load class
        # create object of class
        # while creating object resolve the context
        job_class = self.load_job(job_name)
        context = self.get_context(job_name)
        job: BaseJob = job_class(**{'context': context, 'seed': self.seed})
        job_inputs = job.prepare()
        job_inputs = job_inputs if isinstance(job_inputs, tuple) else tuple([job_inputs])
        job.run(*job_inputs)
        return job

    def run(self, job_sequences):
        for job_name in job_sequences:
            if isinstance(job_name, list):
                # need to execute in parallel
                job_names = job_name
                with concurrent.futures.ThreadPoolExecutor(max_workers=len(job_names)) as executor:
                    futures = {}
                    for _job_name in job_names:
                        futures[executor.submit(
                            self.execute_job, _job_name
                        )] = _job_name

                    for future in concurrent.futures.as_completed(futures):
                        _job_name = futures[future]
                        try:
                            self.context[_job_name] = future.result()
                        except Exception as exc:
                            traceback.print_exception(*sys.exc_info())
                            logger.error('%r generated an exception: %s' % (job_name, exc))
            else:
                # serial execution
                self.context[job_name] = self.execute_job(job_name)
