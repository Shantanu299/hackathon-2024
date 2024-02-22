from app.workflow.jobs.base_job import BaseJob
from app.workflow.jsons import outputs


class Dssat(BaseJob):
    def prepare(self, *args, **kwargs):
        dssat_request = self.seed
        return dssat_request

    def run(self, *args, **kwargs):
        dssat_request = args
        # call DSSAT API to get growth stages
        self.data = outputs.dssat_output  # dssat output
