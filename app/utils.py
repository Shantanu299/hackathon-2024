def find_by_key(data, target):
    """
    Function to recursively find a value of a key in dictionary
    @data: dictionary
    @target: key to which value need to be sought
    @return: value of target key
    """
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


def get_stage_date(data, stage):
    """
    Function to provide date of a particular stage from DSSAT response
    @data: DSSAT output
    @stage: name of stage
    @return: datetime value of a particular stage
    """
    feature_categories = find_by_key(data, 'predictions')
    stage_found_f = False
    for feature_category in feature_categories:
        for feature in feature_category['features']:
            if feature['type'] == 'growth_stage:Ritchie scale' and feature['value'] == stage:
                stage_found_f = True
            if stage_found_f and feature['type'] == 'growth_stage:start_date':
                return feature['value']


def get_growth_stage_date(data):
    """
    function to get growth stage date
    @data: DSSAT output
    @return: Growoth stage datetime
    """
    return get_stage_date(data, 'R6')


def get_emergence_date(data):
    """
    function to get growth stage date
    @data: DSSAT output
    @return: emergence datetime
    """
    return get_stage_date(data, 'VE')
