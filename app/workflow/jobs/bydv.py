import json
import logging

import requests

from app.json_transformer.json_to_json import JSONToJSON
from app.utils import find_by_key, get_emergence_date
from app.workflow.jobs.base_job import BaseJob

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Bydv(BaseJob):
    BYDV_REQUEST = {
        "request_version": "v1.0",
        "fields": [
            {
                "models": [
                    {
                        "name": "bydv",
                        "version": "v1.0"
                    }
                ],
                "location": {
                    "geometry": {
                        "type": "Point",
                        "coordinates": [
                            lambda row_dict: row_dict['long'],
                            lambda row_dict: row_dict['lat'],
                        ]
                    }
                },
                "observations": {
                    "crop_emergence_date": lambda row_dict: row_dict['emergence_date']
                }
            }
        ]
    }

    def prepare(self, *args, **kwargs):
        """
        Function to prepare job or making inputs to run BYDV model
        """
        logger.info("Preparing input for BYDV model API")
        dssat_output = self.context['dssat'].data
        long, lat = find_by_key(self.seed, 'coordinates')
        data = {
            'long': long,
            'lat': lat,
            'emergence_date': get_emergence_date(dssat_output).split('T')[0]
        }
        json_obj = JSONToJSON(self.BYDV_REQUEST)
        bydv_input = json_obj.transform(data)
        return bydv_input

    def run(self, *args, **kwargs):
        """
        Function to run BYDV model on prepared input
        @args: BYDV request
        """
        bydv_input = args
        logger.info(f"BYDV Input: {bydv_input[0]}")
        # call Bydv API to get harvest data
        self.data = requests.request(
            "POST",
            self.ie_prediction_api,
            headers=self.headers,
            data=json.dumps(bydv_input[0])
        ).json()
