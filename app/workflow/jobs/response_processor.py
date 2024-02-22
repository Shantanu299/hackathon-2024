from app.workflow.jobs.base_job import BaseJob


class ResponseProcessor(BaseJob):
    def prepare(self, *args, **kwargs):
        dssat_output = self.context['dssat'].data
        dry_down_output = self.context['dry_down'].data
        bydv_output = self.context['bydv'].data
        return dssat_output, dry_down_output, bydv_output

    def run(self, *args, **kwargs):
        dssat_output, dry_down_output, bydv_output = args
        if dry_down_output['results'][0]['predictions'][-1]['feature_category'] == 'optimal_harvest_time':
            dssat_output['results'][0]['predictions'].append(
                {
                    "feature_category": "best_harvest",
                    "features": [
                        {
                            "type": "best_harvest:date",
                            "value": f"{dry_down_output['results'][0]['predictions'][-1]['features'][0]['value']}"
                        }
                    ]

                }
            )
        else:
            for dry_down_result in dry_down_output['results'][0]['predictions']:
                if dry_down_result['feature_category'] == 'optimal_harvest_time':
                    dssat_output['results'][0]['predictions'].append(
                        {
                            "feature_category": "best_harvest",
                            "features": [
                                {
                                    "type": "best_harvest:date",
                                    "value": f"{dry_down_output['results'][0]['predictions'][-1]['features'][0]['value']}"
                                }
                            ]

                        }
                    )

        self.data = dssat_output
