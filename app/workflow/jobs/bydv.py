import json

import requests

from app.json_transformer.json_to_json import JSONToJSON
from app.utils import find_by_key
from app.workflow.jobs.base_job import BaseJob


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

    def get_emergence_date(self, dssat_output):
        """
        Function to get emergence date from DSSAT output
        @dssat_output: DSSAT output
        @return: emergence date
        """
        feature_categories = find_by_key(dssat_output, 'predictions')
        emergence_f = False
        for feature_category in feature_categories:
            for feature in feature_category['features']:
                if feature['type'] == 'growth_stage:Ritchie scale' and feature['value'] == 'VE':
                    emergence_f = True
                if emergence_f and feature['type'] == 'growth_stage:start_date':
                    return feature['value']

    def prepare(self, *args, **kwargs):
        """
        Function to prepare job or making inputs to run BYDV model
        """
        dssat_output = self.context['dssat'].data
        long, lat = find_by_key(self.seed, 'coordinates')
        data = {
            'long': long,
            'lat': lat,
            'emergence_date': self.get_emergence_date(dssat_output).split('T')[0]
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
        # call Bydv API to get harvest data
        self.data = requests.request(
            "POST",
            self.ie_prediction_api,
            headers=self.headers,
            data=json.dumps(bydv_input[0])
        ).json()
