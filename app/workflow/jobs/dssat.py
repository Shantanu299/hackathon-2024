import json
import requests
from app.workflow.jobs.base_job import BaseJob
from app.workflow.jsons import outputs


class Dssat(BaseJob):
    def prepare(self, *args, **kwargs):
        dssat_request = self.seed
        return dssat_request

    def run(self, *args, **kwargs):
        """
        This function is responsible to call DSSAT Pheno which will provide the growth stage predictions
        @args: DSSAT request
        @return: DSSAT Pheno response
        """
        dssat_request = args
        self.data = requests.request("POST", self.ie_prediction_api, headers=self.headers,
                                     data=json.dumps(dssat_request[0])).json()
