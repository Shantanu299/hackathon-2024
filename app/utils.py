def find_by_key(data, target):
    for key, value in data.items():
        if key == target:
            return value
        elif isinstance(value, list):
            for obj in value:
                if isinstance(obj, dict):
                    target_value = find_by_key(obj, target)
                    if target_value:
                        return target_value
        elif isinstance(value, dict):
            target_value = find_by_key(value, target)
            if target_value:
                return target_value


def get_growth_stage_date(data):
    predictions = data["results"][0]["predictions"]
    for key in predictions:
        for feature in key["features"]:
            if feature["type"] == "growth_stage:Ritchie scale" and feature["value"] == "R6":
                for feat in key["features"]:
                    if feat["type"] == "growth_stage:start_date":
                        return feat["value"].split("T")[0]

