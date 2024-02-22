from app.workflow.jobs.base_job import BaseJob


class DryDown(BaseJob):
    def prepare(self, *args, **kwargs):
        dssat_output = self.context['dssat'].data
        return dssat_output

    def run(self, *args, **kwargs):
        dssat_output = args
        # call DryDown API to get harvest data
        self.data = None  # DryDown output
