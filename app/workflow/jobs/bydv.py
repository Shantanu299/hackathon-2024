from app.workflow.jobs.base_job import BaseJob


class Bydv(BaseJob):
    def prepare(self, *args, **kwargs):
        dssat_output = self.context['dssat'].data
        return dssat_output

    def run(self, *args, **kwargs):
        dssat_output = args
        # call Bydv API to get harvest data
        self.data = None  # Bydv output
