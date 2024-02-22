import json, requests, logging
from app.workflow.jobs.base_job import BaseJob
from app.utils import find_by_key, get_growth_stage_date
from app.json_transformer.json_to_json import JSONToJSON

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DryDown(BaseJob):
    DRY_DOWN_INPUT = {
        "request_version": "v1.0",
        "fields": [
            {
                "models": [
                    {
                        "name": "dry-down",
                        "version": "v1.0"
                    }
                ],
                "location": {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [
                            lambda row_dict: row_dict["long"],
                            lambda row_dict: row_dict["lat"]
                        ]
                    }
                },
                "crop": lambda row_dict: row_dict["crop"],
                "observations": [
                    {
                        "category": "crop_growth_stages",
                        "values": [
                            {
                                "scale": "ritchie",
                                "stage_name": "R6",
                                "date": lambda row_dict: row_dict["date"]
                            }
                        ]
                    }
                ],
                "crop_variety": {
                    "attribute": {
                        "drying_coefficient_k": 0.0336
                    }
                },
                "attributes": {
                    "grain_moisture_at_harvest": lambda row_dict: row_dict["moisture"]
                }
            }
        ]
    }

    def prepare(self, *args, **kwargs):
        """
        Function to prepare job or making inputs to run DryDown model
        """
        dssat_output = self.context['dssat'].data
        long, lat = find_by_key(self.seed, "coordinates")
        data = {
            "lat": lat,
            "long": long,
            "date": get_growth_stage_date(dssat_output),
            "crop": find_by_key(self.seed, "crop"),
            "moisture": 35
        }
        json_obj = JSONToJSON(self.DRY_DOWN_INPUT)
        dry_down_input = json_obj.transform(data)
        return dry_down_input

    def run(self, *args, **kwargs):
        """
        Function to run DryDown model on prepared input
        @args: DryDown request
        """
        dry_down_request = args
        logger.info(f"Drydown request: {dry_down_request}")
        # call DryDown API to get harvest data
        self.data = requests.request(
            "POST",
            self.ie_prediction_api,
            headers=self.headers,
            data=json.dumps(dry_down_request[0])
        ).json()
