import json
import logging

import requests
from app.workflow.jobs.base_job import BaseJob

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Dssat(BaseJob):
    def prepare(self, *args, **kwargs):
        logger.info("Preparing input for DSSAT model API")
        dssat_request = self.seed
        return dssat_request

    def run(self, *args, **kwargs):
        """
        This function is responsible to call DSSAT Pheno which will provide the growth stage
        predictions
        @args: DSSAT request
        """
        dssat_request = args
        logger.info("DSSAT Input: %s", dssat_request[0])
        self.data = requests.request(
            "POST",
            self.ie_prediction_api,
            headers=self.headers,
            data=json.dumps(dssat_request[0])
        ).json()
