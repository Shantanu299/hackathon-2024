from app.workflow.jobs.base_job import BaseJob


class ResponseProcessor(BaseJob):
    def prepare(self, *args, **kwargs):
        dssat_output = self.context['dssat'].data
        dry_down_output = self.context['dry_down'].data
        bydv_output = self.context['bydv'].data
        return dssat_output, dry_down_output, bydv_output

    def run(self, *args, **kwargs):
        dssat_output, dry_down_output, bydv_output = args
        # process response accordingly
        self.data = {"dssat_output": dssat_output, "dry_down_output": dry_down_output, "bydv_output": bydv_output}
