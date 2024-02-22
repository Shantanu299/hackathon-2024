drydown_sample_input = {
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
