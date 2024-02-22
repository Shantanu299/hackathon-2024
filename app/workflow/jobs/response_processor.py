import logging

from app.utils import find_by_key
from app.workflow.jobs.base_job import BaseJob

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ResponseProcessor(BaseJob):
    def prepare(self, *args, **kwargs):
        """
        Function to prepare input for response of prediction API
        """
        logger.info("Preparing input for prediction API output")
        dssat_output = self.context['dssat'].data
        dry_down_output = self.context['dry_down'].data
        bydv_output = self.context['bydv'].data
        return dssat_output, dry_down_output, bydv_output

    def run(self, *args, **kwargs):
        """
        Function to prepare response of prediction API
        @args: tuple of dssat_output, dry_down_output, bydv_output
        """
        dssat_output, dry_down_output, bydv_output = args
        logger.info("Combining DSSAT, Dry-Down and BYDV model outputs")
        ################## DRY-DOWN RESPONSE ################
        dry_down_feature_categories = find_by_key(dry_down_output, 'predictions')
        optimal_harvest_category = list(filter(
            lambda feature_category: feature_category['feature_category'] == 'optimal_harvest_time',
            dry_down_feature_categories))[0]

        dssat_feature_categories = find_by_key(dssat_output, 'predictions')
        dssat_feature_categories.append(
            {
                "feature_category": "best_harvest",
                "features": [
                    {
                        "type": "best_harvest:date",
                        "value": f"{optimal_harvest_category['features'][0]['value']}T00:00:00Z"
                    }
                ]
            }
        )
        ################## BYDV RESPONSE ################
        bydv_feature_categories = find_by_key(bydv_output, 'predictions')
        bydv_risk_warning_features = []
        for feature_category in bydv_feature_categories:
            warning = feature_category['feature_category']
            date = feature_category['features'][0]['value']
            bydv_risk_warning_features.append({
                'type': f'{warning}:date',
                'value': f'{date}T00:00:00Z'
            })
        dssat_feature_categories.append({
            'feature_category': 'bydv_risk',
            'features': bydv_risk_warning_features
        })
        logger.info("ResponseProcessor job is done, returning response in API output")
        self.data = dssat_output
